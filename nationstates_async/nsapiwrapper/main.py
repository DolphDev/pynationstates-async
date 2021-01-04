from requests import Session
from .objects import RateLimit, NationAPI, RegionAPI, WorldAPI, WorldAssemblyAPI, TelegramAPI
from .exceptions import RateLimitReached
from .info import max_safe_requests, ratelimit_max, ratelimit_within, ratelimit_maxsleeps, ratelimit_sleep_time, max_ongoing_requests
from .objects import RateLimit, NationAPI, PrivateNationAPI, RegionAPI, WorldAPI, WorldAssemblyAPI, CardsAPI
from .utils import sleep_thread

import asyncio
import aiohttp

class Api:
    def __init__(self, user_agent, version='11',
        ratelimit_sleep=False,
        ratelimit_sleep_time=ratelimit_sleep_time,
        ratelimit_max=ratelimit_max,
        ratelimit_within=ratelimit_within,
        ratelimit_maxsleeps=ratelimit_maxsleeps,
        max_safe_requests=max_safe_requests,
        ratelimit_enabled=True,
        use_session=True,
        limit_request=True,
        max_ongoing_requests=max_ongoing_requests):
        self.user_agent = user_agent
        self.version = version
        self.ratelimitsleep = ratelimit_sleep
        self.ratelimitsleep_time = ratelimit_sleep_time
        self.ratelimitsleep_maxsleeps = ratelimit_maxsleeps
        self.ratelimit_max = ratelimit_max
        self.ratelimit_within = ratelimit_within
        self.max_safe_requests = max_safe_requests
        self.ratelimit_enabled = ratelimit_enabled
        self.max_ongoing_requests = max_ongoing_requests
        self.use_session = False
        if use_session:
            # Todo remove session usage
            self.session = None
        else:
            self.session = None
        self.xrls = 0
        self.rlobj = RateLimit()
        self.ratelimit_lock = asyncio.Lock()
        self.limit_request = limit_request
        self.__activerequests__ = 0

    def increment_tracker(self):
        self.__activerequests__ = self.__activerequests__ + 1

    def decrement_tracker(self):
        self.__activerequests__ = self.__activerequests__ - 1

    def get_xrls(self):
        return self.rlobj.get_xrls_timestamp()

    def rate_limit(self, new_xrls=1):
        # Raises an exception if RateLimit is either banned 
        self.rlobj.add_xrls_timestamp(new_xrls)

    def _check_ratelimit(self):
        xrls = self.rlobj.get_xrls_timestamp_final()
        return self.rlobj.ratelimitcheck(xrls=xrls,
                amount_allow=self.ratelimit_max,
                within_time=self.ratelimit_within)

    async def check_ratelimit(self):
        "Check's the ratelimit"
        rlflag = self._check_ratelimit()
        if not self.ratelimit_enabled:
            return True
        # Get other async operations a chance to aquire the lock

        if not rlflag:
            if self.ratelimitsleep:
                n = 0
                while not self._check_ratelimit():
                    n = n + 1
                    if n >= self.ratelimitsleep_maxsleeps:
                        if self.max_safe_requests > self.ratelimit_max:
                            break
                        else:
                            return True
                    await sleep_thread(self.ratelimitsleep_time)

                else:
                    return True
            raise RateLimitReached("The Rate Limit was too close the API limit to safely handle this request")
        else:
            return True

    async def __aenter__(self, *args, **kwargs):
        while self.__activerequests__ >= self.max_ongoing_requests:
            # if the user bursts 40+ requests
            # we can't just allow it
            await asyncio.sleep(0.05)
        self.increment_tracker()

    async def __aexit__(self, *args, **kwargs):
        # aexit isn't really async depedent but we want to keep the with syntax
        await asyncio.sleep(0)
        self.decrement_tracker()

    def Nation(self, name):
        return NationAPI(name, self)

    def PrivateNation(self, name, password=None, autologin=None):
        return PrivateNationAPI(name, self, password=password, autologin=autologin)

    def Region(self, name):
        return RegionAPI(name, self)

    def World(self):
        return WorldAPI(self)

    def WorldAssembly(self, chamber):
        return WorldAssemblyAPI(chamber, self)

    def Telegram(self, client_key=None, tgid=None, key=None):
        return TelegramAPI(self, client_key, tgid, key)

    def Cards(self, **kwargs):
        """ Pass request details in kwargs """
        return CardsAPI(self, **kwargs)
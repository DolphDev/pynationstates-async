from requests import Session
from .objects import RateLimit, NationAPI, RegionAPI, WorldAPI, WorldAssemblyAPI, TelegramAPI
from .exceptions import RateLimitReached
from .info import max_safe_requests, ratelimit_max, ratelimit_within, ratelimit_maxsleeps, ratelimit_sleep_time
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
        limit_request=True):
        self.user_agent = user_agent
        self.version = version
        self.ratelimitsleep = ratelimit_sleep
        self.ratelimitsleep_time = ratelimit_sleep_time
        self.ratelimitsleep_maxsleeps = ratelimit_maxsleeps
        self.ratelimit_max = ratelimit_max
        self.ratelimit_within = ratelimit_within
        self.max_safe_requests = max_safe_requests
        self.ratelimit_enabled = ratelimit_enabled
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

    async def get_xrls(self):
        return await self.rlobj.get_xrls_timestamp()

    async def rate_limit(self, new_xrls=1):
        # Raises an exception if RateLimit is either banned 
        async with self.ratelimit_lock:
            await self.rlobj.add_xrls_timestamp(new_xrls)

    async def _check_ratelimit(self):
        server_xrls = await self.get_xrls()
        local_xrls = await self.rlobj.calculate_internal_xrls()
        print('Server:', server_xrls, 'Local', local_xrls)
        xrls = max(server_xrls, local_xrls) if not self.limit_request else server_xrls
        return await self.rlobj.ratelimitcheck(xrls=self.xrls,
                amount_allow=self.ratelimit_max,
                within_time=self.ratelimit_within)

    async def check_ratelimit(self):
        "Check's the ratelimit"
        async with self.ratelimit_lock:
            rlflag = await self._check_ratelimit()
            if not self.ratelimit_enabled:
                return True
            if not rlflag:
                if self.ratelimitsleep:
                    n = 0
                    while not await self._check_ratelimit():
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
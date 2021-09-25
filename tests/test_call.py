import unittest
import nationstates_async as ns
from random import choice
import datetime
USERAGENT = "Automated Testing Builds by Circle CI for the nationstates-async API wrapper by The United Island Tribes. dolphdevgithub@gmail.com"

import os
test_nation = 'Python Nationstates API wrapper'
test_nation_r = 'pynationstates_telegram_recipient'
PASSWORD = os.environ.get('password')
tgid = os.environ.get('telegram_tgid')
key = os.environ.get('telegram_key')
client_key = os.environ.get('telegram_clientkey')
del os
sep_api =  ns.Nationstates(USERAGENT)

joint_api = ns.Nationstates(USERAGENT)
joint_api_enable_beta = ns.Nationstates(USERAGENT, enable_beta=True)
test_nation_nonauth = joint_api.nation(test_nation)
test_auth_nation = joint_api.nation(test_nation, password=PASSWORD)
test_auth_nation_BETA = joint_api_enable_beta.nation(test_nation, password=PASSWORD)

test_nation_r = joint_api.nation(test_nation_r)
issue_nation_1 = joint_api.nation('Pynationstates Issue Farm 1', password=PASSWORD)
issue_nation_2 = joint_api.nation('Pynationstates Issue Farm 2', password=PASSWORD)
issue_nation_3 = joint_api.nation('Pynationstates Issue Farm 3', password=PASSWORD)
issue_nation_zero = joint_api.nation('pynationstates_0_issues_test_nation', password=PASSWORD)
fake_nation = joint_api.nation('FAKE NATION 1 FAKE NATION 1 FAKE NATION 1 FAKE NATION 1')
fake_region = joint_api.region('FAKE REGION 1 FAKE REGION 1 FAKE REGION 1 FAKE REGION 1')


import asyncio
# Used to translate tests written for pynationstates cause I'n kazy
def run_async_call(c):
    rv = {}
    async def do_io(*args):
         rv[0] = await c
    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_io())
    # hack
    return rv.get(0, None)


def grab_id(newfactbookresponse_text):
    part1 = newfactbookresponse_text.split('id=')
    return part1[1].split('">')[0]


class SetupCallTest(unittest.TestCase):

    def test_create_ns(self):
        try:
            api = ns.Nationstates(USERAGENT)
        except Exception as Err:
            self.fail(Err)

class SeperateCallTest(unittest.TestCase):

    def test_nation_call(self):
        try:
            api = sep_api
            mycall = api.nation("testlandia")
            run_async_call(mycall.get_shards(choice(mycall.auto_shards)))
            run_async_call(mycall.get_shards(choice(mycall.auto_shards), full_response=True))

        except Exception as Err:
            self.fail(Err)

    def test_region_call(self):
        try:
            api = sep_api

            mycall = api.region("Balder")
            run_async_call(mycall.get_shards(choice(mycall.auto_shards)))
            run_async_call(mycall.get_shards(choice(mycall.auto_shards), full_response=True))

        except Exception as Err:
            self.fail(Err)

    def test_world_call(self):
        try:
            api = sep_api

            mycall = api.world()
            run_async_call(mycall.get_shards(choice(mycall.auto_shards)))
            run_async_call(mycall.get_shards(choice(mycall.auto_shards), full_response=True))
        except Exception as Err:
            self.fail(Err)


    def test_wa_call(self):
        try:
            api = sep_api

            mycall = api.wa("1")
            run_async_call(mycall.get_shards(choice(mycall.auto_shards)))
            run_async_call(mycall.get_shards(choice(mycall.auto_shards), full_response=True))
        except Exception as Err:
            self.fail(Err)

    def test_cards_indv_call(self):
        try:
            api = sep_api

            mycall = api.cards()
            run_async_call(mycall.individual_cards(1, 1))
            run_async_call(mycall.individual_cards(1, 1, full_response=True))
            run_async_call(mycall.individual_cards(1, 1, 'trades'))
            run_async_call(mycall.individual_cards(1, 1, ns.Shard('trades')))
            run_async_call(mycall.individual_cards(1, 1, (ns.Shard('trades'),)))

            # mycall.get_shards(choice(mycall.auto_shards))
            # mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            raise Err
            self.fail(Err)

    def test_cards_decks_call(self):
        try:
            api = sep_api

            mycall = api.cards()
            run_async_call(mycall.decks(nation_name='testlandia'))
            run_async_call(mycall.decks(nation_name='testlandia', full_response=True))
            run_async_call(mycall.decks(nation_id=1))

            # mycall.get_shards(choice(mycall.auto_shards))
            # mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            self.fail(Err)

    def test_cards_decksinfo_call(self):
        try:
            api = sep_api

            mycall = api.cards()
            run_async_call(mycall.deck_owner_info(nation_name='testlandia'))
            run_async_call(mycall.deck_owner_info(nation_name='testlandia', full_response=True))
            run_async_call(mycall.deck_owner_info(nation_id=1))

            # mycall.get_shards(choice(mycall.auto_shards))
            # mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            self.fail(Err)

    def test_cards_asks_and_bids_call(self):
        try:
            api = sep_api

            mycall = api.cards()
            run_async_call(mycall.asks_and_bids(nation_name='testlandia'))
            run_async_call(mycall.asks_and_bids(nation_name='testlandia', full_response=True))
            run_async_call(mycall.asks_and_bids(nation_id=1))

            # mycall.get_shards(choice(mycall.auto_shards))
            # mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            self.fail(Err)

    def test_cards_collections_call(self):
        try:
            api = sep_api

            mycall = api.cards()
            run_async_call(mycall.collections(nation_name='testlandia'))
            run_async_call(mycall.collections(nation_name='testlandia', full_response=True))
            run_async_call(mycall.collections(nation_id=1))

            # mycall.get_shards(choice(mycall.auto_shards))
            # mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            self.fail(Err)


    def test_cards_auctions_call(self):
        try:
            api = sep_api

            mycall = api.cards()
            run_async_call(mycall.auctions())
            run_async_call(mycall.auctions(full_response=True))

            # mycall.get_shards(choice(mycall.auto_shards))
            # mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            self.fail(Err)



    def test_cards_trades_call(self):
        try:
            api = sep_api

            mycall = api.cards()
            run_async_call(mycall.trades())
            run_async_call(mycall.trades(full_response=True))
            run_async_call(mycall.collections(nation_id=1))

            # mycall.get_shards(choice(mycall.auto_shards))
            # mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            self.fail(Err)

    def test_auto_shard_static_n(self):
        try:
            api = sep_api

            mycall = api.nation("testlandia")
            run_async_call(mycall.fullname)
        except Exception as Err:
            self.fail(Err)

    def test_auto_shard_static_r(self):
        try:
            api = sep_api

            mycall = api.region("balder")
            run_async_call(mycall.numnations)
        except Exception as Err:
            self.fail(Err)

    def test_auto_shard_static_w(self):
        try:
            api = sep_api

            mycall = api.world()
            run_async_call(mycall.numnations)
        except Exception as Err:
            self.fail(Err)

    def test_auto_shard_static_wa(self):
        try:
            api = sep_api

            mycall = api.wa("1")
            run_async_call(mycall.numnations)
        except Exception as Err:
            self.fail(Err)

class ApiJoinTest(unittest.TestCase):

    def test_private_nation(self):
        try:
            run_async_call(test_auth_nation.get_shards('ping'))
        except Exception as Err:
            self.fail(Err)

    def test_exists(self):
        assert run_async_call(fake_nation.exists()) is False
        assert run_async_call(fake_region.exists()) is False
        assert run_async_call(test_auth_nation.exists())


    def test_create_dispatch(self):
        from datetime import datetime
        now = datetime.now
        try:
            resp = run_async_call(test_auth_nation.create_dispatch(title='AUTOMATED ADD DISPATCH TEST', text=str(now()), category=1, subcategory=105, full_response=True))
            dispatch_id = grab_id(resp['data']['nation']['success'])
            resp = run_async_call(test_auth_nation.remove_dispatch(dispatch_id=dispatch_id, full_response=True))

            resp = run_async_call(test_auth_nation.create_dispatch(title='AUTOMATED ADD DISPATCH TEST', text=str(now()), category=1, subcategory=105, full_response=False))
            dispatch_id = grab_id(resp.success)
            resp = run_async_call(test_auth_nation.remove_dispatch(dispatch_id=dispatch_id, full_response=True))

        except Exception as Err:
            print(Err)
            self.fail(Err)

    def test_edit_dispatch(self):
        from datetime import datetime
        now = datetime.now
        try:
            resp = run_async_call(test_auth_nation.create_dispatch(title='AUTOMATED ADD DISPATCH EDIT TEST', text=str(now()), category=1, subcategory=105, full_response=False))
            dispatch_id = grab_id(resp.success)
            resp = run_async_call(test_auth_nation.edit_dispatch(dispatch_id=dispatch_id, title='EDIT TEST', text="THIS POST WAS LAST EDITED AT:" + str(now()), category=1, subcategory=111, full_response=False))
            resp = run_async_call(test_auth_nation.remove_dispatch(dispatch_id=dispatch_id, full_response=True))           
            resp = run_async_call(test_auth_nation.create_dispatch(title='AUTOMATED ADD DISPATCH EDIT TEST', text=str(now()), category=1, subcategory=105, full_response=False))       
            dispatch_id = grab_id(resp.success)            
            resp = run_async_call(test_auth_nation.edit_dispatch(dispatch_id=dispatch_id, title='EDIT TEST', text="THIS POST WAS LAST EDITED AT:" + str(now()), category=1, subcategory=111, full_response=True))
            resp = run_async_call(test_auth_nation.remove_dispatch(dispatch_id=dispatch_id, full_response=True))
        
        except Exception as Err:
            self.fail(Err)

    def test_remove_dispatch(self):
        from datetime import datetime
        now = datetime.now
        try:
            resp = run_async_call(test_auth_nation.create_dispatch(title='AUTOMATED ADD DISPATCH REMOVE TEST', text=str(now()), category=1, subcategory=105, full_response=False))
            dispatch_id = grab_id(resp.success)
            resp = run_async_call(test_auth_nation.remove_dispatch(dispatch_id=dispatch_id))
            resp = run_async_call(test_auth_nation.create_dispatch(title='AUTOMATED ADD DISPATCH REMOVE TEST', text=str(now()), category=1, subcategory=105, full_response=False))
            dispatch_id = grab_id(resp.success)
            resp = run_async_call(test_auth_nation.remove_dispatch(dispatch_id=dispatch_id, full_response=True))
        except Exception as Err:
            self.fail(Err)

    def test_send_rmb(self):
        try:
            run_async_call(test_auth_nation_BETA.send_rmb(test_auth_nation.region, 'Circle CI: Automated Test'))     
        except Exception as Err:
            self.fail(Err)

    def test_telegram_send(self):
        from datetime import datetime
        import time
        now = datetime.now
        try:
            telegram = joint_api.telegram(tgid=tgid, key=key, client_key=client_key) 
            run_async_call(test_nation_r.send_telegram(telegram))
            try:
                run_async_call(test_nation_r.send_telegram(telegram))
                self.fail('API was suppose to block this')
            except ns.nsapiwrapper.exceptions.APIRateLimitBan:
                pass
            try:
                run_async_call(telegram.send_telegram(test_nation_r.name))
            except ns.nsapiwrapper.exceptions.APIRateLimitBan:
                # Just testing code path works - to much wasted time to wait 30 seconds
                pass
        except Exception as Err:
            raise (Err)

    def test_pick_issue_always_fail(self):
        resp = run_async_call(issue_nation_zero.get_shards('issues'))
        if resp.issues is None:     
            pass
        else:
            self.fail('Nation should have no issues')

    def test_pick_issue(self):
        import random

        def pick_random_nation(*apis):
            for api in apis:
                resp = run_async_call(api.get_shards('issues'))
                if resp.issues is None:     
                    continue
                random_issue = random.choice(resp.issues.issue)
                random_issue_id = random_issue.id
                random_option_choice = random.choice(random_issue.option).id
                run_async_call(api.pick_issue(random_issue_id, random_option_choice))
                break
        nations = [issue_nation_1, issue_nation_2, issue_nation_3]
        random.shuffle(nations)
        pick_random_nation(*nations)


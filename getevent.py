from pynostr.relay import Relay
from pynostr.filters import FiltersList, Filters
from pynostr.base_relay import RelayPolicy
from pynostr.message_pool import MessagePool
from pynostr.event import EventKind
import tornado.ioloop
from tornado import gen
import uuid
import json

def getevent(ids=None, kinds=None, authors=None, since=None, until=None, event_refs=None, pubkey_refs=None, limit=None):
    message_pool = MessagePool(first_response_only=False)
    policy = RelayPolicy()
    io_loop = tornado.ioloop.IOLoop.current()
    r = Relay(
        "wss://relay.damus.io",
        message_pool,
        io_loop,
        policy,
        timeout=2
    )

    event_list = []
    filter = FiltersList([Filters(ids=ids, kinds=kinds, authors=authors, since=since, until=until, event_refs=event_refs, pubkey_refs=pubkey_refs, limit=limit)])
    subscription_id = uuid.uuid1().hex
    r.add_subscription(subscription_id, filter)

    try:
        io_loop.run_sync(r.connect)
    except gen.Return:
        pass
    # io_loop.stop()

    while message_pool.has_notices():
        notice_msg = message_pool.get_notice()
        print(notice_msg.content)
    while message_pool.has_events():
        event_msg = message_pool.get_event()
        event = json.loads(str(event_msg.event))
        event_list.append(event)

    return event_list

if __name__ == "__main__":
    # from pynostr.key import PublicKey
    # note = "note1gn882ya9mc5c6f8xyndzvznsg3sxsp06ht6rj5lqfktdgefnaxjq2pm8w2"
    # notehex = PublicKey.from_npub(note).hex()
    # event = getevent(ids=[notehex])
    # # print(event)
    # video = event[0][1]['tags'][1][1]
    # print(video)
    event = getevent(kinds=[6250])
    print(event)
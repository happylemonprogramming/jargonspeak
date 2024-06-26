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
    from pynostr.key import PublicKey
    # note = "note1gn882ya9mc5c6f8xyndzvznsg3sxsp06ht6rj5lqfktdgefnaxjq2pm8w2"
    # notehex = PublicKey.from_npub(note).hex()
    # event = getevent(ids=[notehex])
    # # print(event)
    # video = event[0][1]['tags'][1][1]
    # print(video)
    # npub1hee433872q2gen90cqh2ypwcq9z7y5ugn23etrd2l2rrwpruss8qwmrsv6
    pubkey = "npub10sa7ya5uwmhv6mrwyunkwgkl4cxc45spsff9x3fp2wuspy7yze2qr5zx5p"
    # pubkey = "npub1l2vyh47mk2p0qlsku7hg0vn29faehy9hy34ygaclpn66ukqp3afqutajft" #Pablo
    pubhex = PublicKey.from_npub(pubkey).hex()

    event = getevent(kinds=[31990], authors=[pubhex])
    print(event)
    # tags = event[0][1]['tags']
    # print(len(tags),type(tags))

    # friendhex = '8fe53b37518e3dbe9bab26d912292001d8b882de9456b7b08b615f912dc8bf4a'
    # friendpub = PublicKey.from_hex(friendhex).npub
    # # npub13ljnkd633c7maxatymv3y2fqq8vt3qk7j3tt0vytv90eztwgha9qmfcfhw
    # print(friendpub)

    # [['EVENT', {'id': 'ae446c70be11ab80da0366013b409af65d71bbeba7772d56ea4dfd549b066bd2', 
    #             'pubkey': '7c3be2769c76eecd6c6e27276722dfae0d8ad201825253452153b90093c41654', 
    #             'created_at': 1719333054, 
    #             'kind': 6250, 
    #             'tags': [['e', 'e5ec95fb78eb0825ebc3b1b5dcba3bcc6229c34c719da1b14651719c643b135b'], 
    #                      ['p', 'fa984bd7dbb282f07e16e7ae87b26a2a7b9b90b7246a44771f0cf5ae58018f52']], 
    #                      'content': 'https://privatevideotranslation.s3.us-west-1.amazonaws.com/Swanne5ec95fb78eb0825ebc3b1b5dcba3bcc6229c34c719da1b14651719c643b135b.wav', 
    #                      'sig': 'a1e83546f96c22387d8d9bb34cb1259cda8f83e1119e7b2f9687c17f74d6765e0dcbfef1a4713ceea17b3f3b8c5f196b0820dddfa97b080517148b0027773da0'}]
    #             'content': 'https://privatevideotranslation.s3.us-west-1.amazonaws.com/Swanne5ec95fb78eb0825ebc3b1b5dcba3bcc6229c34c719da1b14651719c643b135b.wav', 
    #             'sig': 'a1e83546f96c22387d8d9bb34cb1259cda8f83e1119e7b2f9687c17f74d6765e0dcbfef1a4713ceea17b3f3b8c5f196b0820dddfa97b080517148b0027773da0'}]
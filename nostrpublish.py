# Libraries
import json
# import ssl
import time
# import uuid
import sys
from pynostr.event import Event
from pynostr.relay_manager import RelayManager
# from pynostr.filters import FiltersList, Filters
# from pynostr.message_type import ClientMessageType
from pynostr.key import PrivateKey
import os
import uuid


# Environment variables
private_key = os.environ["nostrdvmprivatekey"]   

# Relays
relay_manager = RelayManager(timeout=6)
relay_manager.add_relay("wss://nostr-pub.wellorder.net")
relay_manager.add_relay("wss://relay.damus.io")

# Private Key
# private_key = PrivateKey()
# private_object = PrivateKey.from_nsec(private_key)
# private_hex = private_object.hex()
# public_hex = private_object.public_key.hex()

def nostrpost(private_key,kind,content,userinput,usertype):
    private_object = PrivateKey.from_nsec(private_key)
    private_hex = private_object.hex()

    # # Filters
    # filters = FiltersList([Filters(authors=[public_hex], limit=100)])

    # # Subscriptions
    # subscription_id = uuid.uuid1().hex
    # relay_manager.add_subscription_on_all_relays(subscription_id, filters)
        
    if len(sys.argv) > 1:
        kind = sys.argv[1]
        tags = sys.argv[2]
        content = sys.argv[3]

        kind = int(kind)

        # Replace single quotes with double quotes
        tags = tags.replace("'", "\"")

        # Convert the string to a list using JSON
        tags = json.loads(tags)

        event = Event(
                    kind = kind, 
                    tags = tags,
                    content = content
                    )
    elif userinput != None:
        kind = int(kind)
        tags = [["k", f"{userinput}"], ["d", f"{usertype}"]]
        # Replace single quotes with double quotes
        tags = str(tags)
        tags = tags.replace("'", "\"")

        # Convert the string to a list using JSON
        tags = json.loads(tags)
        # tags = json.dumps(tags)
        print(tags)
        event = Event(
                    kind = kind, 
                    tags = tags,
                    content = content
                    )
        print(event)
    else:
        # Simple Note
        event = Event(
                    kind = kind, 
                    content = content
                    )
        
        
        # Speech to Text Event
        # event = Event(
        #             kind = 65002, 
        #             tags = [
        #                         [ "i", "http://here-and-now.info/audio/rickastley_artists.mp3", "text" ],
        #                         [ "output", "text/plain" ]
        #                     ],
        #             content = ''
        #             )

        # Summarize Event
        # event = Event(
        #               kind = 65003, 
        #               tags = [['i', 'The story of my life is that I try and I fail until I eventually succeed.', 'text']],
        #               content = ''
        #               )

        # Image Event
        # ['EVENT', 
        #  {'id': 'cd4672b1673868216b57c50f302b5ba6cad5e75a7728c604664d9838492237e5', 
        #   'pubkey': '558497db304332004e59387bc3ba1df5738eac395b0e56b45bfb2eb5400a1e39', 
        #   'created_at': 1691110127, 
        #   'kind': 65005, 
        #   'tags': [['i', 'Dramatic+ 8k wallpaper medium shot waist up photo of fearsome young witch wearing intricate robes and silver pauldrons, magic+, high detail, detailed background, detailed eyes, wild hair, wind blown hair, cinematic lighting, masterpiece, best quality, high contrast, soft lighting, backlighting, bloom, light sparkles, chromatic aberration, smooth, sharp focus', 'text'], 
        #            ['params', 'negative_prompt', 'hat, old, child, childlike, 3d, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name'], 
        #            ['params', 'size', '768', '768'], 
        #            ['wss://relay.damus.io', 'wss://relay.snort.social', 'wss://blastr.f7z.xyz', 'wss://nostr.mutinywallet.com', 'wss://relayable.org'], 
        #            ['bid', '5000', '10000']], 
        #            'content': 'Generate a Picture based on the attached prompt', 
        #            'sig': '2ae18593540d2c0eb2f27692279bf5d0f65ecb2c975385e4fe436fd3e44b7baf11a9756ae842d7003ff73496e66c56c3f4f937ebf011703d70d5e6bc91bf6b5e'}]


    # Publish
    event.sign(private_hex)
    relay_manager.publish_event(event)
    relay_manager.run_sync()
    time.sleep(5) # allow the messages to send
    while relay_manager.message_pool.has_ok_notices():
        ok_msg = relay_manager.message_pool.get_ok_notice()
        print(ok_msg)
    while relay_manager.message_pool.has_events():
        event_msg = relay_manager.message_pool.get_event()
        print(event_msg.event.to_dict())
    print('Event Published')
    return "Event Published"

if __name__ == '__main__':
    kind = 31990
    content = "{\"name\": \"Swanbot\", \"image\": \"https://primal.b-cdn.net/media-cache?s=o&a=1&u=https%3A%2F%2Fm.primal.net%2FIyOX.png\", \"about\": \"Data Vending Machine Generating Speech from Text with a Legendary Voice\", \"encryptionSupported\": false, \"cashuAccepted\": false, \"nip90Params\": {\"language\": {\"required\": false, \"values\": []}}}"
    kindsupport = "5250"
    randomid = uuid.uuid1().hex
    nostrpost(private_key,kind,content,kindsupport, randomid)
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

def nostrreply(private_key,kind,content,noteID,pubkey_ref,bolt11=None, amount=None, eventInput=None):
    private_object = PrivateKey.from_nsec(private_key)
    private_hex = private_object.hex()

    # # Filters
    # filters = FiltersList([Filters(authors=[public_hex], limit=100)])

    # # Subscriptions
    # subscription_id = uuid.uuid1().hex
    # relay_manager.add_subscription_on_all_relays(subscription_id, filters)

    # Post Construction
    kind = int(kind)
    # "tags":[["e","b2..."],["p","be..."]]
    if bolt11!=None and amount!=None:
        tags = [["status", "payment-required", "Swann DVM"], ["amount", f"{amount}", f"{bolt11}"], ["e", f"{noteID}"], ["p", f"{pubkey_ref}"]]
    elif eventInput!=None:
        tags = [["i", f"{eventInput}", "event"]]
    elif isinstance(pubkey_ref, list):
        tags = [["e", f"{noteID}"]]
        for pubkey in pubkey_ref:
            tags.append(["p", f"{pubkey}"])
    else:
        tags = [["e", f"{noteID}"], ["p", f"{pubkey_ref}"]]
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
    kind = 5250
    content = 'Builders be buildin'
    noteID = '976abdfffa674d7ddb60ec269a10241d9df2a7d815cf1df4d4a8e1eccabce550'
    pubkey_ref = 'be7358c4fe50148cccafc02ea205d80145e253889aa3958daafa8637047c840e'
    nostrreply(private_key,kind,content,noteID,pubkey_ref,eventInput=noteID)
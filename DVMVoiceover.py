# Outside libaries
from pynostr.key import PublicKey
import time
import json
import math
import re

# Internal programs
from getevent import getevent
from lightningpay import *
from nostrreply import nostrreply
from translatevideo_gladia import translatevideo
from videofunctions import detectvideo
from aivoicecreator import aispeech
from cloud import *

# Set bot Public Key
botpubkey = 'npub1hee433872q2gen90cqh2ypwcq9z7y5ugn23etrd2l2rrwpruss8qwmrsv6' #TODO: update to DVM key
pubhex = PublicKey.from_npub(botpubkey).hex()
private_key = os.environ["nostrdvmprivatekey"]

# Initialize lists
completed_events = [] # TODO: should persist over time
quoted_events = {}

# Loop through active events
condition = True
since = round(time.time())

# Run continuously
while condition:
    event_list = getevent(kinds=[5250], since=since) # added since condition to keep filter current replies
    for event in event_list:
        eventID = event[1]['id']
        print(event)
        if 'event' in str(event[1]['tags']):
            # NOTE: Pubkey reference should have target language in content
            if eventID not in completed_events and eventID not in quoted_events:
                # Get public key reference for user
                pubkey_ref = event[1]['pubkey']
                for tag in event[1]['tags']:
                    # if tag[0] == 'p':
                    #     pubkey_ref = tag[1]
                    # if tag[0] == 'e':
                    #     target_eventID = tag[1]
                    if tag[0] == 'i' and tag[2]=='event':
                        target_eventID = tag[1]

                # User folder creation
                visitorid = uuid.uuid1().hex
                # filepath = os.getcwd() + f'/files/{visitorid}/' # Doesn't work locally
                filepath = f'files/{visitorid}/' # Doesn't work on Heroku
                if os.path.exists(filepath):
                    pass
                else:
                    os.makedirs(filepath)

                # Get target content
                target_event = getevent(ids=[target_eventID])[0]
                print('Target Event:', target_event)
                # Isolate content
                targetContent = target_event[1]['content']
                print('Target Event Content:', targetContent)

                # Get names instead of npubs
                if 'nostr:npub' in targetContent:
                    npubs = re.findall(r'nostr:npub(\S+)', targetContent)
                    for npub in npubs:
                        pubkey = 'npub'+npub
                        pubhex = PublicKey.from_npub(pubkey).hex()
                        metadata = getevent(kinds=[0],authors=[pubhex])
                        name = json.loads(metadata[0][1]['content'])['name']
                        targetContent = targetContent.replace('nostr:npub'+npub,name)

                # Save content to local file in user folder
                with open(filepath+f'Swannbot{eventID}', 'w', encoding='utf-8') as file:
                    file.write(targetContent)

                # Get pricing and save invoice id
                costPerCharacter = 0.30/1000
                contentLength = len(targetContent)
                quote = costPerCharacter*contentLength #TODO: update from 0.01
                if quote < 0.01:
                    quote = 0.01
                lninv, conv_rate, invid = lightning_quote('0.01',f'Swann DVM') #TODO: dynamic pricing ($0.01 for testing)
                amount = math.ceil(quote/float(conv_rate)*100000000*1000)
                quoted_events[eventID] = invid
                print('Invoice Created')

                # Reply with invoice
                nostrreply(private_key, kind=7000, content='\U0001F34B', noteID=eventID, pubkey_ref=pubkey_ref, bolt11=lninv, amount=amount)
                break

        # Check invoice status and save ID for status check 
        if eventID in quoted_events:
            invid = quoted_events[eventID]
            status = invoice_status(invid)
            print('Quote Status:', status)

            # Provide content if paid
            if status == 'PAID':
                # Get public key reference for user
                pubkey_ref = event[1]['pubkey']
                # for tag in event[1]['tags']:
                #     if tag[0] == 'p':
                #         pubkey_ref = tag[1]
                
                # Transform content
                with open(filepath+f'Swannbot{eventID}', 'r', encoding='utf-8') as file:
                    text = file.read()
                aispeech(text=text, voice='30onnySJpZzctyufqBND', output = filepath+f'Swann{eventID}.wav')
                link = serverlink(filepath+f'Swann{eventID}.wav', f'Swann{eventID}.wav')
                public_url = re.findall(r'https?://\S+?\.wav', link)[0]

                # Post paid content
                nostrreply(private_key,kind=6250,content=public_url,noteID=eventID,pubkey_ref=pubkey_ref)
                
                # Update lists
                quoted_events.pop(eventID)
                print('Quoted Events:', len(quoted_events))
                completed_events.append(eventID)
                print('Completed Events:', len(completed_events))

    print('waiting...')
    time.sleep(3)

'''
PROGRAM LOGIC:
if someone @'s npub with language selection, then offer invoice
add event id to quoted events
listen to invoice id for payment

if invoice is paid, then offer translated content
remove from quoted events (listening)
add event id to completed events (no listening)
'''
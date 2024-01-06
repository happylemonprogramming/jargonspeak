# Outside libaries
from pynostr.key import PublicKey
import time
import re

# Internal programs
from getevent import getevent
from lightningpay import *
from nostrreply import nostrreply
from translatevideo_gladia import translatevideo
from videofunctions import detectvideo

# Set bot Public Key
botpubkey = 'npub1hee433872q2gen90cqh2ypwcq9z7y5ugn23etrd2l2rrwpruss8qwmrsv6' #TODO: update to DVM key
pubhex = PublicKey.from_npub(botpubkey).hex()
private_key = os.environ["nostrdvmprivatekey"]

# Set available languages
languages = {
  "English": "EN-US",
#   "English (UK)": "EN-GB",
  "Spanish": "ES",
  "German": "DE",
  "Japanese": "JA",
  "Korean": "KO",
  "Polish": "PL",
  "Portuguese": "PT-PT",
  "Portuguese (Brazil)": "PT-BR",
  "Romanian": "RO",
  "Slovak": "SK",
  "Swedish": "SV",
  "Turkish": "TR",
  "Ukrainian": "UK",
  "Chinese": "ZH",
  "Bulgarian": "BG",
  "Czech": "CS",
  "Danish": "DA",
  "Greek": "EL",
  "Finnish": "FI",
  "Indonesian": "ID",
  "Italian": "IT"
}

# Initialize lists
completed_events = [] # TODO: should persist over time
quoted_events = {}

# Loop through active events
condition = True
since = round(time.time())

# Run continuously
while condition:
    event_list = getevent(kinds=[1],pubkey_refs=[pubhex], since=since) # added since condition to keep filter current replies
    for event in event_list:
        # NOTE: Pubkey reference should have target language in content
        eventID = event[1]['id']
        eventContent = event[1]['content']
        print('Event Content:', eventContent)

        if eventID not in completed_events and eventID not in quoted_events:
            for language in list(languages.keys()):
                if language in event[1]['content']:
                    # Get public key reference for user
                    for tag in event[1]['tags']:
                        if tag[0] == 'p':
                            pubkey_ref = tag[1]
                        if tag[0] == 'e':
                            target_eventID = tag[1]

                    # User folder creation
                    visitorid = uuid.uuid1().hex
                    # filepath = os.getcwd() + f'/files/{visitorid}/' # Doesn't work locally
                    filepath = f'files/{visitorid}/' # Doesn't work on Heroku
                    if os.path.exists(filepath):
                        pass
                    else:
                        os.makedirs(filepath)

                    # Get target video content
                    target_event = getevent(ids=[target_eventID])[0]
                    print('Target Event:', target_event)
                    # Isolate video link
                    targetContent = target_event[1]['content']
                    print('Target Event Content:', targetContent)
                    video = re.findall(r'https?://\S+\.mp4', targetContent)[0] # assumes single url
                    print('Video url:', video)
                    
                    # Detect video duration
                    max_length = 300
                    filename = 'video.mp4'
                    duration = detectvideo(video=video,max_length=max_length,filepath=filepath, filename=filename)
                    print('Video Duration:', duration)

                    # Get pricing and save invoice id
                    costPerMinute = 0.79
                    durationInMinutes = round(int(duration)/60)
                    quote = costPerMinute*durationInMinutes #TODO: update from 0.01
                    target_language = languages[language]
                    print('Target Language Code:', target_language)
                    lninv, conv_rate, invid = lightning_quote('0.01',f'Video Translation Quote ({durationInMinutes} minutes)') #TODO: dynamic pricing ($0.01 for testing)
                    quoted_events[eventID] = invid
                    print('Invoice Created')

                    # Reply with invoice
                    nostrreply(private_key,kind=1,content=lninv,noteID=eventID,pubkey_ref=pubkey_ref)
                    break

        # Check invoice status and save ID for status check 
        if eventID in quoted_events:
            invid = quoted_events[eventID]
            status = invoice_status(invid)
            print('Quote Status:', status)

            # Provide content if paid
            if status == 'PAID':
                # Get public key reference for user
                for tag in event[1]['tags']:
                    if tag[0] == 'p':
                        pubkey_ref = tag[1]

                # Translate content
                response = translatevideo(video=filepath+filename, voice='Clone', captions=True, filepath=filepath, filename=filename, language=target_language, cclanguage=target_language)
                translated_video = response[2]
                public_url = re.findall(r'https?://\S+?\.mp4', translated_video)[0]
                # Post paid content
                nostrreply(private_key,kind=1,content=public_url,noteID=eventID,pubkey_ref=pubkey_ref)
                
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
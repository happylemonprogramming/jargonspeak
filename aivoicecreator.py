from elevenlabs import generate, set_api_key, save
import os
import requests
import time

set_api_key(os.environ.get('elevenlabsapikey'))

def aispeech(text=None,voice='Bella',output='speechoutput.wav',text_file=None):
    start = time.time()
    voiceList = ['Rachel', 'Domi', 'Bella', 'Antoni', ' Elli', 'Josh', 'Arnold', 'Adam', 'Sam']
    putin = '2tfqZPGDSMcLjnTVNO2o'
    vader = 'mzzyrHBdOjyMhiNl1rT7'
    # rachel is meh, domi is female, bella best story teller, elli is kiddish
    # josh is rugged, arnold is like a car salesman, energetic, adam is more news anchor, sam is teenager (male)

    if text_file != None:
        # Open the text file in read mode
        with open(text_file, 'r') as file:
            # Read the entire contents of the file into a variable
            text = file.read()

    # for voice in voiceList:
    audio = generate(
    text=text,
    voice=voice,
    # voice=voiceList[voice_index],
    # model="eleven_monolingual_v1"
    model="eleven_multilingual_v2"
    )
    save(audio, output)
    print(f"AI speech created successfully! ({round(time.time()-start,2)}s)")
    return output


def addvoice(audio,name):
    start = time.time()
    url = "https://api.elevenlabs.io/v1/voices/add"

    headers = {
    "Accept": "application/json",
    "xi-api-key": os.environ.get('elevenlabsapikey')}

    data = {
        'name': name}

    files = [
        ('files', (audio, open(audio, 'rb'), 'audio/mpeg'))]

    response = requests.post(url, headers=headers, data=data, files=files)
    output = response.text
    print(f"New AI voice added successfully! ({round(time.time()-start,2)}s)")
    return output


def deletevoice(voiceid):
    start = time.time()
    url = f"https://api.elevenlabs.io/v1/voices/{voiceid}"

    headers = {
    "Accept": "application/json",
    "xi-api-key": os.environ.get('elevenlabsapikey')
    }

    requests.delete(url, headers=headers)

    print(f"Voice removed successfully! ({round(time.time()-start,2)}s)")

def subscriptioninfo():
    url = "https://api.elevenlabs.io/v1/user/subscription"

    headers = {
    "Accept": "application/json",
    "xi-api-key": os.environ.get('elevenlabsapikey')
    }

    response = requests.get(url, headers=headers)

    return response.json()

if __name__ == '__main__':
    # voicepath = r'C:\Users\clayt\Documents\Programming\translait\output\iamyourfather\vocals.wav'
    # vader = addvoice(voicepath,'Vader')
    # print(vader)
    aispeech(text='Luke, I am your father.',voice='mzzyrHBdOjyMhiNl1rT7',output='vader.wav',text_file=None)


    # {'tier': 'creator', 
    #  'character_count': 67386, 
    #  'character_limit': 100029, 
    #  'can_extend_character_limit': True, 
    #  'allowed_to_extend_character_limit': False, 
    #  'next_character_count_reset_unix': 1696393711, 
    #  'voice_limit': 30, 
    #  'max_voice_add_edits': 95, 
    #  'voice_add_edit_counter': 44, 
    #  'professional_voice_limit': 1, 
    #  'can_extend_voice_limit': False, 
    #  'can_use_instant_voice_cloning': True, 
    #  'can_use_professional_voice_cloning': True, 
    #  'currency': 'usd', 'status': 'active', 
    #  'next_invoice': {'amount_due_cents': 2200, 'next_payment_attempt_unix': 1696411711}, 
    #  'has_open_invoices': False}
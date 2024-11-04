from elevenlabs import generate, set_api_key, save
import os
import requests
import time

# Languages
# 🇺🇸 English (USA)
# 🇬🇧 English (UK)
# 🇦🇺 English (Australia)
# 🇨🇦 English (Canada)
# 🇯🇵 Japanese
# 🇨🇳 Chinese
# 🇩🇪 German
# 🇮🇳 Hindi
# 🇫🇷 French (France)
# 🇨🇦 French (Canada)
# 🇰🇷 Korean
# 🇧🇷 Portuguese (Brazil)
# 🇵🇹 Portuguese (Portugal)
# 🇮🇹 Italian
# 🇪🇸 Spanish (Spain)
# 🇲🇽 Spanish (Mexico)
# 🇮🇩 Indonesian
# 🇳🇱 Dutch
# 🇹🇷 Turkish
# 🇵🇭 Filipino
# 🇵🇱 Polish
# 🇸🇪 Swedish
# 🇧🇬 Bulgarian
# 🇷🇴 Romanian
# 🇸🇦 Arabic (Saudi Arabia)
# 🇦🇪 Arabic (UAE)
# 🇨🇿 Czech
# 🇬🇷 Greek
# 🇫🇮 Finnish
# 🇭🇷 Croatian
# 🇲🇾 Malay
# 🇸🇰 Slovak
# 🇩🇰 Danish
# 🇮🇳 Tamil
# 🇺🇦 Ukrainian


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

def texttospeech(text, voice='Bella', output='speechoutput.wav'):
    import requests

    CHUNK_SIZE = 1024
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"

    headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": os.environ.get('elevenlabsapikey')
    }

    data = {
    "text": text,
    "model_id": "eleven_multilingual_v2"
    }

    response = requests.post(url, json=data, headers=headers)
    with open(output, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

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
    print(f"AI Voice POST Request! ({round(time.time()-start,2)}s)")
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

def speechtospeech(audio_file_path,voice_id):
    # ERROR: {"detail":{"status":"voice_not_found",
    # "message":"A voice for the voice_id mzzyrHBdOjyMhiNl1rT7 was not found."}}
    # Set the API endpoint URL and replace {voice_id} with the actual voice ID
    api_url = f"https://api.elevenlabs.io/v1/speech-to-speech/{voice_id}"

    # Make the POST request with the audio file
    files = {'audio': open(audio_file_path, 'rb')}
    payload = {"model_id": "eleven_multilingual_v2"}
    headers = {
    "Accept": "application/json",
    "xi-api-key": os.environ.get('elevenlabsapikey')
    }

    response = requests.post(api_url, files=files, json=payload, headers=headers)

    # Print the response
    print(response.text)

if __name__ == '__main__':
    # voicepath = r'C:\Users\clayt\Documents\Programming\translait\output\iamyourfather\vocals.wav'
    # vader = addvoice(voicepath,'Vader')
    # print(vader)
    # aispeech(text='Luke, I am your father.',voice='mzzyrHBdOjyMhiNl1rT7',output='vader.wav',text_file=None)
    # addvoice(r'C:\Users\clayt\Documents\Programming\jargonspeak\files\9ba0465e6faf11eebef618ff0f367121\original.mp4', 'jobs')
    # audio_file_path = 'files/cf18fe2f8af211eeb2ff18ff0f367121/extractedaudio.mp3'
    # voice_id = 'uO96UIs3QYEaGBuCRGiS'
    # from audiofunctions import audioslicing
    # audioslicing(audio_file_path, 7, 30, output = 'cheatcode.mp3')
    # voice_id = addvoice(audio_file_path,'jobbyjobs')
    # import json
    # voice = json.loads(voice_id)
    # speechtospeech('cheatcode.mp3','mzzyrHBdOjyMhiNl1rT7')
    # print(texttospeech('can you take me higher? to a place where blind men see. lets go there. lets make some mistakes, come on.','30onnySJpZzctyufqBND'))
    info = subscriptioninfo()
    character_count = info['character_count']
    character_limit = info['character_limit']
    print(info)
    print(character_count,character_limit)
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
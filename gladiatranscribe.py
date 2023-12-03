import requests
import os

api_key = os.environ['gladiaapikey']
# Can't do YouTube Shorts
def urlgladiatranscribe(url,target_language):
    headers = {
        'x-gladia-key': api_key,
    }

    files = {
        'audio_url': (None, url),
        'target_translation_language': (None, target_language),
        'toggle_diarization': (None, 'true'),
        'toggle_direct_translate': (None, 'true'),
    }

    response = requests.post('https://api.gladia.io/audio/text/audio-transcription/', headers=headers, files=files)
    return response.text

def localgladiatranscribe(path, target_language):
    headers = {
        'x-gladia-key': api_key,
    }

    files = {
        'target_translation_language': (None, target_language),
        'toggle_diarization': (None, 'true'),
        'toggle_direct_translate': (None, 'true'),
        'video': open(path, 'rb'),
    }

    response = requests.post('https://api.gladia.io/video/text/video-transcription/', headers=headers, files=files)
    return response.text


if __name__ == '__main__':
    import time
    start = time.time()
    url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    target_language = 'english'
    output = urlgladiatranscribe(url,target_language)
    end = time.time()
    print(output)
    # with open('gladiaoutput.txt', 'w', encoding='utf-8') as file:
    #     file.write(str(output))

    print(end-start)

    # with open('gladiaoutput.txt', 'r', encoding='utf-8') as file:
    #     output = file.read()

    transcripts = []
    starts = []
    ends = []
    speaker = []
    import json
    output = json.loads(output)
    for group in output['prediction']:
        transcripts.append(group['transcription']) 
        starts.append(group['time_begin'])
        ends.append(group['time_end'])
        speaker.append(group['speaker'])

    print(transcripts)
    print(starts)
    print(ends)
    print(speaker)
    print(len(transcripts), len(starts), len(ends),len(speaker))
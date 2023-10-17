from deepgram import Deepgram
import os
import requests
import time

DEEPGRAM_API_KEY = os.environ["deepgramapikey"]
PROJECT_ID = '8489a89c-7cd3-4d3e-8fe4-dbcdfdeb98c0'

'''
Requests to Whisper are limited to 15 concurrent requests with a paid plan and 5 concurrent requests with the pay-as-you-go plan.
Long audio files are supported up to a maximum of 20 minutes of processing time (the maximum length of the audio depends on the size of the Whisper model).
'''

# Transcription Languages
# https://developers.deepgram.com/docs/languages-overview
languages = {'English': 'en', 'Australia': 'en-AU', 'United Kingdom': 'en-GB', 'India': 'en-IN', 'New Zealand': 'en-NZ', 'United States': 'en-US', 
            'Danish': 'da',
            'French': 'fr', 'French Canadian': 'fr-CA', 
            'German': 'de', 
            'Hindi': 'hi', 'Roman Script': 'hi-Latn', 
            'Portuguese': 'pt', 'Brazil': 'pt-BR', 'Portugal': 'pt-PT', 
            'Russian': 'ru', 
            'Spanish': 'es', 'Latin America': 'es-419', 
            'Turkish': 'tr',
            # BETA
            'Chinese (BETA)': 'zh', 'China (BETA)': 'zh-CN', 'Taiwan (BETA)': 'zh-CN',
            'Dutch (BETA)': 'nl', 'Flemish (BETA)': 'nl',
            'Indonesian (BETA)': 'id',
            'Italian (BETA)': 'it',
            'Japanese (BETA)': 'ja',
            'Korean (BETA)': 'ko',
            'Norwegian (BETA)': 'no',
            'Polish (BETA)': 'pl',
            'Swedish (BETA)': 'sv',
            'Tamil (BETA)': 'ta',
            'Ukranian (BETA)': 'uk'}

def localtranscription(localpath, language):
    start = time.time()

    # Initializes the Deepgram SDK
    deepgram = Deepgram(DEEPGRAM_API_KEY)
    
    english = {'en', 'en-AU', 'en-GB', 'en-IN', 'en-NZ', 'en-US'}
    enhanced = {'da','fr','de','hi','pt','pt-BR','pt-PT','es','es-419','nl','it','ja','ko','no','pl','sv','ta'}
    if language in english:
        # model = 'nova'
        # model = 'whisper-large'
        model='nova-2-ea'
    elif language in enhanced:
        # model = 'enhanced'
        model = 'whisper-large'
    else:
        # model = 'base'
        model = 'whisper-large'

    # Open the audio file
    with open(localpath, 'rb') as audio:
        # ...or replace mimetype as appropriate
        source = {'buffer': audio, 'mimetype': 'audio/wav'} # doesn't seem to impact videos
        response = deepgram.transcription.sync_prerecorded(source, {'punctuate': True, 'smart_format': True, 'language':language, 'diarize': True,'model':model}) #tier=base&model=video or model=whisper-large

    print(f"Transcribed url successfully! ({round(time.time()-start,2)}s)")

    return response

def getDeepgramTranscription(p_url):
    start = time.time()
    # Use this to get subtitles in English
    url = "https://api.deepgram.com/v1/listen?model=nova-2-ea&language=en&punctuate=true&diarize=true&smart_format=true"
    # url = "https://api.deepgram.com/v1/listen?model=whisper-large&language=en&punctuate=true&diarize=true&smart_format=true"

    # Use this to get subtitles in the same language as the audio/video
    # url = "https://api.deepgram.com/v1/listen?model=whisper-large&detect_language=true"

    payload = {
        "url": p_url
    }

    headers = {
        "Authorization": 'Token ' + DEEPGRAM_API_KEY,
        "content-type": "application/json"
    }

    response = requests.request("POST", url, headers=headers, json=payload)
    output = response.json()

    print(f"Transcribed url successfully! ({round(time.time()-start,2)}s)")

    return output

def extract_sentences_from_srt(srt):
    # Save subtitle lines in variable
    with open(srt, 'r') as file:
        subtitles = file.readlines()
    
    # Initialize list and sort through subtitle lines
    words = []
    for word in subtitles:
        try:
            int(word)
        except:
            if ':' in word:
                pass
            elif word.strip() == '':
                pass
            else:
                words.append(word.strip())

    # Convert the list of words into a single string
    text = ' '.join(words)
    return text

def convert_to_srt(data, path, level='sentence'):
    start = time.time()
    print('Data input type: ', type(data))
    word_level = data['words']
    sentence_level = data['paragraphs']['paragraphs']

    def format_time(seconds):
        # Convert seconds to hours, minutes, seconds, milliseconds format
        hours, remainder = divmod(seconds, 3600)
        minutes, remainder = divmod(remainder, 60)
        seconds, milliseconds = divmod(remainder, 1)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{int(milliseconds*1000):03d}"

    if level == 'word':
        # Word-Level
        data = word_level
        output_filename = path + 'word_level.srt'
        with open(output_filename, 'w') as f:
            for i, entry in enumerate(data, start=1):
                start_time = format_time(entry['start'])
                end_time = format_time(entry['end'])
                subtitle_text = entry['punctuated_word']
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{subtitle_text}\n\n")

    elif level == 'sentence':
        # Sentence-Level
        output_filename = path + 'sentence_level.srt'

        # intialize lists
        sentences = []
        texts = []
        starts = []
        ends = []
        i = 0

        # gather all paragraphs into unified list
        for paragraph in sentence_level:
            sentences.append(paragraph['sentences'])

        # create text list, start list and end list
        for sentence in sentences:
            for text in sentence:
                # TODO: Add sentence subtitles
                texts.append(text['text'])
                starts.append(text['start'])
                ends.append(text['end'])

        with open(output_filename, 'w') as f:
            for i, entry in enumerate(texts, start=1):
                start_time = format_time(starts[i-1])
                end_time = format_time(ends[i-1])
                subtitle_text = texts[i-1]
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{subtitle_text}\n\n")
            
    print(f"Created .srt successfully! ({round(time.time()-start,2)}s)")
    return output_filename

if __name__ == '__main__':
    # Hyperlink Function
    # p_url = 'https://db9c2d0e80dc9774067d0f439aa504a7.cdn.bubble.io/f1692677290753x434684319755118660/RPReplay_Final1692675241.MP4'
    # # p_url = 'https://s3.amazonaws.com/appforest_uf/f1678940868271x564994871606250500/aistorytelling.py%20-%20Untitled%20%28Workspace%29%20-%20Visual%20Studio%20Code%202023-01-02%2011-12-25.mp4'
    # # p_url = 'https://www.youtube.com/watch?v=X--l6Qy5Tb0'
    # output = getDeepgramTranscription(p_url)
    
    # Local Function
    path = r'C:\Users\clayt\Documents\Programming\jargonspeak\video.mp4'
    output = localtranscription(path,languages['English'])
        
    # Output Reading
    print('Output: ', output, type(output))
    # keys = [key for key in output]
    # print(keys)
    # raw_text = output['results']['channels'][0]['alternatives'][0]['transcript']
    # subtitle_data = output['results']['channels'][0]['alternatives'][0]
    paragraphs = output['results']['channels'][0]['alternatives'][0]['paragraphs']['paragraphs']
    # words = output['results']['channels'][0]['alternatives'][0]['words']
    # print('Raw Text: ', raw_text)
    # print('Subtitle Data: ', subtitle_data)
    print('Paragraphs: ', paragraphs)
    # print('Words: ', words)
    with open('yodatranscript.txt', 'w', encoding='utf-8') as file:
        file.write(str(output))
    print('Video transcribed')
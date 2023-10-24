import requests
import os

# Language Pairs:
# DE (German)
# EN (English)
# ES (Spanish)
# FR (French)
# IT (Italian)
# JA (Japanese)
# NL (Dutch)
# PL (Polish)
# PT (Portuguese)
# RU (Russian)
# ZH (Chinese)

# Replace '[yourAuthKey]' with your actual DeepL-Auth-Key
auth_key = os.environ['deeplapikey']

def texttranslate(text, language):
    # API endpoint and data
    url = 'https://api-free.deepl.com/v2/translate'
    headers = {
        'Authorization': f'DeepL-Auth-Key {auth_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'text': [
            text
        ],
        'target_lang': language
    }

    # Send the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check the response
    if response.status_code == 200:
        translation_data = response.json()
        translations = translation_data['translations']
        for translation in translations:
            response = translation['text']
            print(response)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
    return response

if __name__ == '__main__':
    texttranslate('mamba mentality is the only mentality', 'es')
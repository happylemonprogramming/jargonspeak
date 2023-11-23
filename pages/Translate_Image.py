from readreplacetext import *
from linegroup import linegroup
from deepltranslate import texttranslate
from removetext import removetext
from videofunctions import downloadvideo
import requests
import streamlit as st
import uuid
import os

st.set_page_config(
    page_title='jargonspeak',
    page_icon=':earth_americas:'
)

def downloadContent(url, local_filename):
	try:
		# Send a GET request to the URL
		response = requests.get(url, stream=True)
		response.raise_for_status()  # Check for any errors in the response

		# Open a local file for writing in binary mode
		with open(local_filename, 'wb') as local_file:
			for chunk in response.iter_content(chunk_size=8192):
				if chunk:  # Filter out keep-alive new chunks
					local_file.write(chunk)

	except Exception as e:
		print(f"An error occurred: {e}")

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

st.title(':frame_with_picture: Image Translator')
st.info('''
        Unlimited translations at $0.05/image.
        ''')
meme_link = st.text_input('Image link or meme url:')
target_language = st.selectbox('Language:', [key for key in languages])
language = languages[target_language]
click = st.button(':rocket: Launch!')
if click:
    with st.spinner('Translating...'):
        visitorid = uuid.uuid1().hex
        # filepath = os.getcwd() + f'/files/{visitorid}/' # Doesn't work locally
        filepath = f'files/{visitorid}/' # Doesn't work on Heroku
        if os.path.exists(filepath):
            pass
        else:
            os.makedirs(filepath)
            os.makedirs(filepath+'frames')
        # Inputs
        input_image_path = f'{filepath}local.png'
        downloadvideo(meme_link,input_image_path) #meme download
        noTextImage = f'{filepath}notext.png'

        # Read the meme and gather text
        textdetection = textdetect(input_image_path)

        # Group words into lines with a buffer of 5 pixels
        rows, bounds = linegroup(textdetection, buffer=5)

        translated_lines = []
        for row in rows:
            translated_line = texttranslate(row, language)
            translated_lines.append(translated_line)

        removetext(input_image_path,noTextImage)

        textreplace2(noTextImage,f'{filepath}final.png',translated_lines,bounds)
		
    st.image(f'{filepath}final.png')
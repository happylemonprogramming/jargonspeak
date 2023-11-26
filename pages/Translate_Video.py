# Web Option
# from deeptranscribe import languages
# from deepltranslate import languages
import streamlit as st
import os
import time
from translatevideo import translatevideo
from translateaudio import translateaudio
from videofunctions import split, detectvideo
from audiofunctions import audioslicing
from lightningpay import *
from qrcodegenerator import *
import uuid

st.set_page_config(
    page_title='jargonspeak',
    page_icon=':earth_americas:'
)

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

# Front Page
st.title(":vhs: Video Translator")
st.info('''
        Unlimited captions at $0.06/minute.\n
        Unlimited dubbing at $0.79/minute.
        ''')

# st.text('Unlimited dubbing at $0.79/minute for all languages. Voice cloning included.')
# st.text('Unlimited subtitling at $0.06/minute for all languages.')

video_url = st.text_input('Video url or YouTube link:')
uploaded_file = st.file_uploader("Upload a file:", type=["mp4","mov"])

# col1, col2 = st.columns(2)
# with col1:
#     clip_start = int(st.number_input('Clip Start (optional)', min_value=0, step=1))
#     voice = st.selectbox('Voice:', ['None','Clone','Bella','Josh'])
#     # voice = 'Speaker'
#     if voice != 'None':
#         speech = st.selectbox('Voice Language:', [key for key in languages])
#         language = languages[speech]
#     else:
#         language = None
# with col2:
#     clip_end = int(st.number_input('Clip End (optional)',min_value=0, step=1))
#     cc = st.toggle('Subtitles')
#     # cc = False
#     if cc == True:
#         subselection = st.selectbox('Subtitle Language:', [key for key in languages])
#         cclanguage = languages[subselection]
#     else:
#         cclanguage = None
if 'jpg' in video_url:
    print('jpg')

clip = st.toggle('Clip')
if clip:
    clip_start = int(st.number_input('Start', min_value=0, step=1))
    clip_end = int(st.number_input('End',min_value=0, step=1))
else:
    clip_start = 0
    clip_end = 0
# voice = st.selectbox('Voice:', ['None','Clone','Bella','Josh'])
voice = st.toggle('Voice')

if voice:
    voice = 'Clone'
    speech = st.selectbox('Audio language:', [key for key in languages])
    language = languages[speech]
else:
    language = None
cc = st.toggle('Subtitles')
# cc = False
if cc == True:
    subselection = st.selectbox('Subtitle language:', [key for key in languages])
    cclanguage = languages[subselection]
else:
    cclanguage = None

# promo = st.text_input('Enter Promo Code (optional):')
promo = 'superspecialcode'

# Voice & Subtitle logic path
# if voice or cc:
    # check = st.checkbox('I understand this application is experimental and AI content can be unpredictable.')
click = st.button(':rocket: Launch!')
if click:
        with st.spinner('Downloading video...'):
            # User folder
            visitorid = uuid.uuid1().hex
            print('User: ', visitorid)
            # filepath = os.getcwd() + '/files/'
            filepath = os.getcwd() + f'/files/{visitorid}/' # Doesn't work locally
            # filepath = f'files/{visitorid}/' # Doesn't work on Heroku
            if os.path.exists(filepath):
                pass
            else:
                os.makedirs(filepath)
            # Uploaded file detection
            if uploaded_file is not None:
                # # Unique identifier folder path creation
                # visitorid = uuid.uuid1().hex
                # filepath = os.getcwd() + f'/files/{visitorid}/'
                # if os.path.exists(filepath):
                #     pass
                # else:
                #     os.makedirs(filepath)

                # File type detection
                filetype = uploaded_file.name[-4:]
                if filetype.lower() == '.mp3':
                    filename = 'original.mp3'
                    video = filepath+filename
                    file_contents = uploaded_file.read()
                    with open(filepath+filename, "wb") as f:
                        f.write(file_contents)

                if filetype.lower() == '.wav':
                    pass

                if filetype.lower() == '.mp4' or filetype.lower() == '.mov':
                    filename = 'original.mp4'
                    video = filepath+filename
                    file_contents = uploaded_file.read()
                    with open(filepath+filename, "wb") as f:
                        f.write(file_contents)
                    # if ".mov" in filetype:
                    #     video = VideoFileClip(filename)
                    #     # Save it as .mp4
                    #     # filename = filename[:-4]+".mp4"
                    #     video.write_videofile(filename, codec="libx264")

            # URL file detection
            if video_url:
                print('URL Detected')
                if 'note' in video_url:
                    print('Note Detected')
                    from pynostr.key import PublicKey
                    from getevent import getevent
                    notehex = PublicKey.from_npub(video_url).hex()
                    event = getevent(ids=[notehex])
                    nostr_video = event[0][1]['tags'][1][1]
                    video_url = nostr_video
                    print('The Nostr url: ', video_url)
    
                video = video_url


            filetype = video[-4:]
            if filetype.lower() == '.mp3':
                filename = 'original.mp3'
            if filetype.lower() == '.mp4' or 'youtube' in video:
                filename = 'original.mp4'

            if os.path.exists(filepath):
                pass
            else:
                os.makedirs(filepath)

            # Get duration & download if less than max length
            max_length = 3600 #hard limit of 1-hour for now
            if clip_end != 0:
                duration = clip_end-clip_start
                if duration < 0:
                    raise Exception('Start time cannot be after end time.')
                detectvideo(video=video,max_length=max_length,filepath=filepath, filename=filename)
            elif (clip_end-clip_start) < 0:
                raise Exception('Start time cannot be after end time.')
            else:
                duration = detectvideo(video=video,max_length=max_length,filepath=filepath, filename=filename)
            video = filepath+filename

        with st.spinner('Pending lightning invoice...'):
            # $0.1000/min Moises (Vocal Background Split)
            # $0.0043/min Deepgram (Transcription)
            # $0.0250/1,000 characters DeepL (Translation) (+$5.49/month)
            # $0.3000/1,000 characters Elevenlabs (AI Voiceover) (+$22/month)
            # $0.0230/GB Amazon S3
            # $0.0100/hour Heroku
            if cc and voice == False:
                cost = 0.005+0.025 # $/MIN Deepgram + DeepL
                margin = 0.03 # $/MIN
                price = round((cost+margin)*duration/60,2)
            # if cc and voice == 'None' and cclanguage == 'EN-US':
            #     cost = 0.005 # $/MIN Deepgram
            #     margin = 0.005 # $/MIN
            #     price = round((cost+margin)*duration/60,2)
            else:
                cost = 0.43 # $/MIN Moises + Deepgram + DeepL + Elevenlabs
                margin = 0.36 # $/MIN
                price = round((cost+margin)*duration/60,2)

            # Route for Lightning Address Generation and Conversion Rate
            quote = lightning_quote(price, 'Jargonspeak!🔥')
            lninv = quote[0]
            conv_rate = quote[1]
            invid = quote[2]
            dictionary = {"lninv": lninv, 'btcusdrate': conv_rate, "invoiceId": invid}

            # Lightning QR Code
            binaryimagedata = QR_Code(lninv, filepath+visitorid+'.png')

            # Check invoice status
            invoice_time = 60
            placeholder1 = st.empty()
            placeholder2 = st.empty()
            placeholder3 = st.empty()
            placeholder4 = st.empty()
            placeholder5 = st.empty()
            inv_status = invoice_status(invid)
            while True:
                if inv_status == 'UNPAID' and promo.lower() != 'superspecialcode' and invoice_time>=1:
                    placeholder1.warning(f'Send ${price:.2f} to Translate {duration}s of Content')
                    placeholder2.warning(f'Time remaining on invoice: {invoice_time}s')
                    placeholder3.image(binaryimagedata)
                    placeholder4.code(lninv)
                    inv_status = invoice_status(invid)
                    invoice_time -= 1
                    time.sleep(1)
                elif invoice_time < 1:
                    placeholder1.empty()
                    placeholder2.empty()
                    placeholder3.empty()
                    placeholder4.empty()
                    raise Exception('Invoice expired, try again. :(')
                    # placeholder5.error('Invoice expired, try again. :(')
                elif inv_status == 'PAID' or promo.lower() == 'superspecialcode':
                    placeholder1.empty()
                    placeholder2.empty()
                    placeholder3.empty()
                    placeholder4.empty()
                    placeholder5.success(f'Paid ${price:.2f} to Translate {duration}s of Content! 🤖')
                    break
                else:
                    st.error('Invoicing error, try again :(')

        # Run translation
        with st.spinner('Running... This may take a few minutes.'):
            start = time.time()
            filename = filename.strip().replace(' ','')
            if 'mp4' in filename or 'mov' in filename:
                if clip_end != 0:
                    print('Media path: ', video)
                    split(video, filepath+'cropped.mp4', clip_start, clip_end)
                    filename = 'cropped.mp4'
                    video = filepath+filename
                response = translatevideo(video, voice=voice, captions=cc, filepath=filepath, filename=filename, language=language, cclanguage=cclanguage)
            elif 'mp3' in filename or 'wav' in filename:
                if clip_end != 0:
                    print('Media path: ', video)
                    audioslicing(video, clip_start, clip_end, filepath+'cropped.mp3')
                    filename = 'cropped.mp3'
                    video = filepath+filename
                response = translateaudio(video, voice=voice, filepath=filepath, filename=filename, language=language)
            formatted_time = time.strftime("%H:%M:%S", time.gmtime(time.time()-start))
            print(f"Total program ran successfully! ({formatted_time})")
            # print(f"Total program ran successfully! ({round((time.time()-start)/60.00,2)}min)")

        # Show video & download button
        placeholder4.empty()
        st.success('Here is the translated media:')
        if 'mp4' in filename or 'mov' in filename:
            st.video(filepath+'jargonspeak_'+filename)
        elif 'mp3' in filename or 'wav' in filename:
            st.audio(filepath+'jargonspeak_'+filename)
        st.link_button(label='Download .mp4', url=response[2]) # Video Download from AWS
        if cc:
            st.link_button(label='Download .srt', url=response[3]) # Subtitle Download from AWS
        # with open(filepath+'jargonspeak_'+filename, 'rb') as file: # Memory Download
        #     # Read the binary data from the file
        #     binary = file.read()
        # st.download_button(label='Download', data=binary, file_name='jargonspeak.mp4', mime='video/mp4')

        # Check accuracy relative to transcription based on minimum character changes
        original_text = response[1]
        from deeptranscribe import getDeepgramTranscription, localtranscription
        # text = getDeepgramTranscription(response[2])
        text = localtranscription(filepath+'jargonspeak_'+filename, 'en-us')
        new_text = text['results']['channels'][0]['alternatives'][0]['transcript']
        from levenshteinalgorithm import calculate_similarity
        similarity = calculate_similarity(original_text, new_text)
        print(f'{similarity:.2f}% Accurate to Transcription')
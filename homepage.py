# Web Option
# from deeptranscribe import languages
# from deepltranslate import languages
import streamlit as st
import os
import time
from translatevideo import translatevideo
from lightningpay import *
from videofunctions import detectvideo
from qrcodegenerator import *
import uuid

languages = {
  "English (USA)": "EN-US",
  "English (UK)": "EN-GB",
  "Spanish": "ES",
  "German": "DE",
  "Japanese": "JA",
  "Korean": "KO",
  "Polish": "PL",
  "Portuguese (Portugal)": "PT-PT",
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
st.title("Automated AI Audio/Video Dubbing")
st.text('Translate, caption or voiceover any video')
video_url = st.text_input('Paste YouTube or video link:')
uploaded_file = st.file_uploader("Upload a file:", type=["mp4","mov"])
# voice = st.selectbox('Voice:', ['None','Speaker','Bella','Josh'])
voice = 'Speaker'
speech = st.selectbox('Language:', [key for key in languages])
language = languages[speech]
# cc = st.toggle('Subtitles') #TODO: work on subtitles
cc = False
promo = st.text_input('Enter Promo Code:')

# Voice & Subtitle logic path
if voice != 'None' or cc:
    check = st.checkbox('I understand this application is experimental and AI content can be unpredictable.')
    click = st.button('Launch!')
    # TODO: add dynamic dubbing pricing using bitcoin
    if click and check:
        with st.spinner('Downloading video...'):
            # Uploaded file detection
            if uploaded_file is not None:
                # Unique identifier folder path creation
                visitorid = uuid.uuid1().hex
                filepath = os.getcwd() + f'/files/{visitorid}/'
                if os.path.exists(filepath):
                    pass
                else:
                    os.makedirs(filepath)

                # File type detection
                filetype = uploaded_file.name[-4:]
                if filetype.lower() == '.mp3':
                    pass
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
                video = video_url
                # Existing file detection
                visitorid = uuid.uuid1().hex
                # filepath = os.getcwd() + '/files/'
                filepath = os.getcwd() + f'/files/{visitorid}/'
                filename = 'original.mp4'
                if os.path.exists(filepath):
                    pass
                else:
                    os.makedirs(filepath)

            # Get duration & download if less than max length
            duration = detectvideo(video=video,max_length=1000000,filepath=filepath, filename=filename)
            video = filepath+filename

        with st.spinner('Pending lightning invoice...'):
            cost = 0.33
            margin = 0.17
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
            inv_status = invoice_status(invid)
            while True:
                if inv_status == 'UNPAID' and promo.lower() != 'superspecialcode' and invoice_time>=1:
                    placeholder1.warning(f'Send ${price:.2f} to Translate {duration}s of Content')
                    placeholder2.warning(f'Time remaining on invoice: {invoice_time}s')
                    placeholder3.image(binaryimagedata)
                    inv_status = invoice_status(invid)
                    invoice_time -= 1
                    time.sleep(1)
                elif invoice_time < 1:
                    placeholder1.empty()
                    placeholder2.empty()
                    placeholder3.empty()
                    placeholder4.error('Invoice expired, try again. :(')
                elif inv_status == 'PAID' or promo.lower() == 'superspecialcode':
                    placeholder1.empty()
                    placeholder2.empty()
                    placeholder3.empty()
                    placeholder4.success(f'Paid ${price:.2f} to Translate {duration}s of Content! 🤖')
                    break
                else:
                    st.error('Invoicing error, try again :(')

        # Run translation
        with st.spinner('Running... This may take a few minutes.'):
            start = time.time()
            filename = filename.strip().replace(' ','')
            response = translatevideo(video, voice=voice, captions=cc, filepath=filepath, filename=filename, language=language)
            print(f"Total program ran successfully! ({round((time.time()-start)/60.00,2)}s)")

        # st.success('Bookmark this link to the video for future reference:')
        # st.code(response[2])

        # Show video & download button
        placeholder4.empty()
        st.success('Here is the translated video:')
        st.video(filepath+'jargonspeak_'+filename)
        with open(filepath+'jargonspeak_'+filename, 'rb') as file:
            # Read the binary data from the file
            binary = file.read()
        st.download_button(label='Download', data=binary, file_name='jargonspeak.mp4', mime='video/mp4')
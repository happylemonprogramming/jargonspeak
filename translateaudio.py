from deeptranscribe import *
from aivoicecreator import *
from audiofunctions import *
from videofunctions import *
from deepltranslate import *
from audiosplitter import *
from cloud import *
import json
import os
import glob
import time

def translateaudio(audio, voice='Bella', filepath='files/', filename= 'video.mp4', language='en'):
	totalstart = time.time()
	start = time.time()
	# STEP #0: Split audio into background & vocals______________________________________________________________________
	# Separate Audio
	# extractedaudio = filepath+'extractedaudio.mp3'
	vocalspath = filepath+'vocals.wav'
	backgroundpath = filepath+'background.wav'
	# extract_audio(video, extractedaudio)
	vocals, background = splitaudio(audio)
	downloadvideo(vocals, vocalspath)
	downloadvideo(background, backgroundpath)
	end = time.time()
	splitaudiotime = end-start

	# STEP #1: Take vocals and transcribe to timed text translation______________________________________________________
	# Transcribe video to text
	start = time.time()
	# text = localtranscription(vocalspath, 'en') # English is the most reliable for timing (see next Step for translation)
	try:
		text = getDeepgramTranscription(vocals)
		paragraphs = text['results']['channels'][0]['alternatives'][0]['paragraphs']['paragraphs']
	except:
		text = getDeepgramTranscription(vocals, model='whisper-large')
		paragraphs = text['results']['channels'][0]['alternatives'][0]['paragraphs']['paragraphs']

	print(text)
	# TODO: split speakers into timed list/dictionary to individually train for each voice in media
	# Open the file in write mode and save 'text' to it
	with open(filepath+'transcript.txt', 'w', encoding='utf-8') as file:
		file.write(str(text))
	print('Video transcribed')

	raw_text = text['results']['channels'][0]['alternatives'][0]['transcript']
	subtitle_data = text['results']['channels'][0]['alternatives'][0]
	words = text['results']['channels'][0]['alternatives'][0]['words']

	# intialize lists
	sentences = []
	transcripts = []
	texts = []
	starts = []
	ends = []
	i = 0

	# Sentence Level
	# gather all paragraphs into unified list
	for paragraph in paragraphs:
		sentences.append(paragraph['sentences'])

	# create text list, start list and end list
	for sentence in sentences:
		for group in sentence:
			transcripts.append(group['text'])
			starts.append(group['start'])
			ends.append(group['end'])
	end = time.time()
	transcribetime = end-start
	
	# # Word Level [Tonality between words is too different and doesn't flow well at all]
	# # gather all paragraphs into unified list
	# for word in words:
	# 	print(word)
	# 	# words.append(phrase['word'])
	# 	texts.append(word['punctuated_word'])
	# 	starts.append(word['start'])
	# 	# ends.append(word['end'])
	# print('Texts length: ', len(texts))
	# print('Starts length: ', len(starts))

	# STEP #1.5: Translate transcription with a separate API for greater accuracy________________________________________
	# This step helps with word timing since Deepgram translations can be timed inconsistently
	start = time.time()
	if language != 'EN-US':
		for transcript in transcripts:
			print(transcript)
			text = texttranslate(transcript, language)
			print(text)
			texts.append(text)
		print('Transcripts: ', transcripts)
		print('Texts: ', texts)
	else:
		texts = transcripts
	end = time.time()
	translatetime = end-start

	# STEP #3: Create AI voice__________________________________________________________________________________________
	aistart = time.time()
	if voice:
		info = subscriptioninfo()
		character_count = info['character_count']
		character_limit = info['character_limit']
		# if character_count<character_limit:
		if True:
			print('New audio requested')

			# # extract video audio
			# extract_audio(filepath+filename, audio_filename=filepath+'videovoice.wav')

			# Use speaker voice if elected (always True currently)
			if voice == 'Clone': # TODO: need to figure out how to train for multiple speakers
				voice = json.loads(addvoice(vocalspath, 'Clone'))
				print('Voice:', voice)

				# Filesize error prevention
				file_size = os.path.getsize(vocalspath)
				target_size = 10 * 1024 * 1024  # 10MB
				audio = AudioSegment.from_file(vocalspath, format="wav")

				# Calculate the duration for a 10MB audio clip (in milliseconds)
				target_duration = (target_size / (file_size * 1.0)) * len(audio)
				while 'detail' in voice and voice['detail']['status'] == 'upload_file_size_exceeded':
					# ERROR {"detail":{"status":"upload_file_size_exceeded",
					# "message":"A uploaded file is too large, please upload files with a maximum of 11MB."}}

					# TODO: evaluate/compare time to train vs. 61 second clip
					# Trim the audio to the desired size
					trimmed_audio = audio[:int(target_duration)]

					# # Trim the audio to the desired duration
					# trimmed_audio = audio[:61 * 1000]

					# Export the trimmed audio as a WAV file
					learningpath = filepath+'voicelearning.wav'
					trimmed_audio.export(learningpath, format="wav")

					# Remeasure for print debug
					file_size = os.path.getsize(learningpath)
					print('Updated File size: ', file_size)
					target_duration *= 0.90 # Keep reducing by 10% until error subsides
					
					# Retrieve result
					voice = json.loads(addvoice(learningpath, 'Clone'))
					print('Voice: ', voice)

					# Successful path (otherwise forever looping until filesize accepted)
					if 'voice_id' in voice:
						voice = voice['voice_id']
						print('Voice ID: ', voice)
						break

				# Voice added without upload error
				else:
					voice = voice['voice_id']
					print(voice, type(voice))

			# Make ai voice for text
			i = 0
			for text in texts:
				# print(text)
				# Create voice from text
				aispeech(text=text, voice=voice, output = filepath+f'AI{i}.wav')
				i += 1
			print('Speech Files Created')

			# Speed up AI voiceover (if needed) to avoid interference
			i = 0
			for start in starts:
				inputfile = filepath+f'AI{i}.wav'
				AIaudio = AudioSegment.from_file(inputfile)
				AIduration = float(len(AIaudio) / 1000) # seconds
				OGduration = float(ends[i]-start) # seconds
				speed = round(AIduration/OGduration,2)
				outputfile = filepath+f'{i}.wav'
				audiospeed(inputfile, outputfile, speed) #FFMPEG cannot edit existing files (safety), thus a new naming convention
				i += 1
				
			# Prepend silence to AI voiceover based on start time
			i = 0
			for start in starts:
				duration = int(float(start)*1000)
				print('Compare times: ', str(start)+'s vs. '+str(duration)+'ms')
				addsilence(filepath+f'{i}.wav', filepath+f'{i}.wav', duration=duration)
				i += 1

			# Overlay audio prepended AI audio over one another for all texts
			i = 0
			for text in texts:
				if i+1 >= len(texts):
					break
				try:
					overlay_audio(filepath+f'{i+1}.wav', filepath+f'{i}.wav', filepath+f'{i+1}.wav')
					i += 1
				except FileNotFoundError as e:
					print(f'Error: {e}')
					break  # Break the loop if a file is not found

			# Final AI voice audio path
			new_audio = filepath+f'{len(texts)-1}.wav'

		else:
			pass # intended to cause error because new_audio is undefined (if character limit exceeded on 11Labs)
	else:
		new_audio = None
		print('No new audio requested')
	aiend = time.time()
	aivoicetime = aiend-aistart
	# STEP #4: Combine AI vocals with background and add to video_______________________________________________________	
	# Combine background with AI voice:
	start = time.time()
	overlay_audio(backgroundpath, new_audio, filepath+'jargonspeak_'+filename)
	end = time.time()
	audiooverlaytime = end-start
	# STEP #5: Cloud storage of video file______________________________________________________________________________
	# TODO: need to figure out permissions and link expiration; may be needed if filesize is too large to download
	start = time.time()
	jargonlink = serverlink(new_audio, 'jargonspeak_'+filename)
	# jargonlink = None
	end = time.time()
	cloudtime = end-start
	# STEP #6: Delete voice and remove files____________________________________________________________________________
	start = time.time()
	# Use glob to find all .wav files in the directory
	wav_files = glob.glob(os.path.join(filepath, "*.wav"))
	# Use glob to find all .mp4 files in the directory
	original_file = glob.glob(os.path.join(filepath, "original.mp4"))

	# Clear voice library space
	deletevoice(voice)

	# Iterate through the list of files and delete each one
	# for wav_file in wav_files:
	# 	os.remove(wav_file)
	# TODO: ERROR file still in use (subprocess.popen.(deletefiles)?)
	# for mp4_file in original_file:
	# 	os.remove(mp4_file)
	end = time.time()
	cleanuptime = end-start
	totalend = time.time()
	totaltime = totalend-totalstart
	timedictionary = {'splitaudiotime': f'{splitaudiotime}s', 'transcribetime': f'{transcribetime}s', 'translatetime': f'{translatetime}s', 'aivoicetime': f'{aivoicetime}s', 'videocompiletime': f'{audiooverlaytime}s', 'cloudtime': f'{cloudtime}s', 'cleanuptime': f'{cleanuptime}s', 'totaltime': f"{totaltime}s"}
	print(timedictionary)
	return new_audio, raw_text, jargonlink

if __name__ == '__main__':
	# Julie's folder automation
	# filepath = r'C:\Users\clayt\Videos\Video Translation\Julie Translations\Originals/'
	# mp4_files = glob.glob(os.path.join(filepath, "*.mp4"))
	# for file in mp4_files:
	# 	filename = os.path.basename(file)
	# 	translatevideo(file, voice='Clone', captions=False, filepath=filepath, filename=filename, language='EN-US')

	# Test playground
	audio = r'C:\Users\clayt\Documents\Programming\jargonspeak\audioslice.mp3'
	translateaudio(audio, voice='Clone', filepath='files/bitcoin_audible/', filename= 'sample.mp3', language='es')

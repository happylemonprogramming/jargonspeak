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

def translatevideo(video, voice='Bella', captions=False, filepath='files/', filename= 'video.mp4', language='EN-US', cclanguage=None):
	totalstart = time.time()

	if os.path.exists(filepath):
		pass
	else:
		os.makedirs(filepath)

# STEP #0: Split audio into background & vocals______________________________________________________________________
	start_time = time.time()
	# Separate Audio
	if captions and voice == False:
		pass # Best way to keep it cheap; can use else function for captions, but adds $0.10/min
	else:
		extractedaudio = filepath+'extractedaudio.mp3'
		vocalspath = filepath+'vocals.wav'
		backgroundpath = filepath+'background.wav'
		# Get audio from media
		extract_audio(video, extractedaudio)
		# Split into vocals and background
		vocals, background = splitaudio(extractedaudio)
		# Download vocals and background audio locally
		downloadvideo(vocals, vocalspath)
		downloadvideo(background, backgroundpath)
	end_time = time.time()
	splitaudiotime = end_time-start_time

# STEP #1: Take vocals and transcribe to timed text translation______________________________________________________
	# Transcribe video to text
	start_time = time.time()
	# Subtitles Only
	if captions and voice == False:
		text = localtranscription(video, 'en') # English is the most reliable for timing (see next Step for translation)
	# Vocals hyperlink preserved for web transcription
	else:
		text = getDeepgramTranscription(vocals)
	print(text)

	# TODO: split speakers into timed list/dictionary to individually train for each voice in media
	
	# Open the file in write mode and save 'text' to it
	with open(filepath+'transcript.txt', 'w', encoding='utf-8') as file:
		file.write(str(text))
	print('Video transcribed')

	# intialize lists
	sentences = []
	transcripts = []
	speakers = []
	texts = []
	cctexts = []
	starts = []
	ends = []
	i = 0

	raw_text = text['results']['channels'][0]['alternatives'][0]['transcript']
	subtitle_data = text['results']['channels'][0]['alternatives'][0]
	words = text['results']['channels'][0]['alternatives'][0]['words']
	paragraphs = text['results']['channels'][0]['alternatives'][0]['paragraphs']['paragraphs']
	
	# Sentence Level
	# gather all paragraphs into unified list
	for paragraph in paragraphs:
		sentences.append(paragraph['sentences'])
		for sentence in paragraph['sentences']:
			speakers.append(paragraph['speaker'])

	# create text list, start list and end list
	for sentence in sentences:
		# {'sentences': [{'text': 'Speaking of Kobe, you brought up, you know, being a fan and growing up in this in in our generation, our era of basketball being in SoCal, and you get to watch him up close and personal.', 'start': 0.08, 'end': 9.62}, {'text': "Like, what what's your favorite or best moment playing against Cole?", 'start': 10.075, 'end': 13.855}], 'speaker': 0, 'num_words': 48, 'start': 0.08, 'end': 13.855},
		# {'sentences': [{'text': 'like, oh, shit.', 'start': 101.39, 'end': 101.95}], 'speaker': 0, 'num_words': 3, 'start': 101.39, 'end': 101.95},
		for group in sentence:
			transcripts.append(group['text']) #no idea if this is going to work or not
			starts.append(group['start'])
			ends.append(group['end'])

	# Initialize speaker count and timing lists
	speakercount = 0
	begin = {0:[]}
	finish = {0:[]}
	body = {0:[]}

	for paragraph in paragraphs:
		# Count speakers
		speaker = paragraph['speaker']
		if speaker > speakercount:
			speakercount = speaker
			begin[speaker] = []
			finish[speaker] = []
			body[speaker] = []
		# Create start end lists for each speaker
		speaker = paragraph['speaker']
		# starts[speaker].append(paragraph['start'])
		# ends[speaker].append(paragraph['end'])
		for text in paragraph['sentences']:
			body[speaker].append(text['text'])
			begin[speaker].append(text['start'])
			finish[speaker].append(text['end'])


	for speaker in range(speakercount+1):
		# Combine the lists into tuples
		combined_data = list(zip(body[speaker], begin[speaker], finish[speaker]))

		# Sort based on the difference between end and start values
		sorted_data = sorted(combined_data, key=lambda x: x[2] - x[1], reverse=True)

		# Unpack the sorted data into separate lists
		sorted_text, sorted_start, sorted_end = zip(*sorted_data)
		body[speaker] = sorted_text
		begin[speaker] = sorted_start
		finish[speaker] = sorted_end

	for speaker in begin:
		i = 0
		total_duration = 0
		for start in begin[speaker]:
			# Slice audio for each speaker, up to 5 minutes
			end = finish[speaker][i]
			clip_duration = end - start
			total_duration += clip_duration
			i+=1
			if os.path.exists(filepath+f'speaker{speaker}'):
				pass
			else:
				os.makedirs(filepath+f'speaker{speaker}')
			if clip_duration > 1:
				audioslicing(f'{filepath}vocals.wav', start, end, output = filepath+f'speaker{speaker}/audioslice{i}.mp3')

			if total_duration > 61:
				print('Threshold!')
				break
		

	# # Initialize speaker count and timing lists
	# speakercount = 0
	# begin = {0:[]}
	# finish = {0:[]}
	# body = {0:[]}

	# for paragraph in paragraphs:
	# 	# Count speakers
	# 	speaker = paragraph['speaker']
	# 	if speaker > speakercount:
	# 		speakercount = speaker
	# 		begin[speaker] = []
	# 		finish[speaker] = []
	# 		body[speaker] = []
	# 	# Create start end lists for each speaker
	# 	speaker = paragraph['speaker']
	# 	# starts[speaker].append(paragraph['start'])
	# 	# ends[speaker].append(paragraph['end'])
	# 	for text in paragraph['sentences']:
	# 		body[speaker].append(text['text'])
	# 		begin[speaker].append(text['start'])
	# 		finish[speaker].append(text['end'])

	# # Rearrange in order of longest clip to shortest clip for speed
	# for speaker in range(speakercount):
	# 	# Combine the lists into tuples
	# 	combined_data = list(zip(body[speaker], begin[speaker], finish[speaker]))

	# 	# Sort based on the difference between end and start values
	# 	sorted_data = sorted(combined_data, key=lambda x: x[2] - x[1], reverse=True)

	# 	# Unpack the sorted data into separate lists
	# 	sorted_text, sorted_start, sorted_end = zip(*sorted_data)
	# 	body[speaker] = sorted_text
	# 	begin[speaker] = sorted_start
	# 	finish[speaker] = sorted_end

	# for speaker in begin:
	# 	i = 0
	# 	total_duration = 0
	# 	for start in begin[speaker]:
	# 		# Slice audio for each speaker, up to 1 minute
	# 		end = sorted_end[i]
	# 		clip_duration = end - start
	# 		total_duration += clip_duration
	# 		i+=1
	# 		# print('Span: ', start, end)
	# 		# print('Clip Duration:', clip_duration)
	# 		# print('Total Duration:', total_duration)
	# 		if os.path.exists(filepath+f'speaker{speaker}'):
	# 			pass
	# 		else:
	# 			os.makedirs(filepath+f'speaker{speaker}')
	# 		if clip_duration > 1:
	# 			audioslicing(f'{filepath}vocals.wav', start, end, output = filepath+f'speaker{speaker}/audioslice{i}.mp3')
	# 		else:
	# 			pass
	# 		if total_duration > 61: # 61 seconds of voice training data
	# 			print('Threshold!')
	# 			break
		

	for speaker in range(speakercount+1):
		# Use glob to find all .mp3 files in the directory
		speaker_files = glob.glob(os.path.join(filepath+f'speaker{speaker}/', "*.mp3"))
		speaker_path = filepath+f'speaker{speaker}.mp3'
		print(speaker_files)
		# Iterate through the list of files
		combined_audio = AudioSegment.silent(duration=0)
		for mp3 in speaker_files:
			# Assuming you want to combine all MP3 files into a single audio file
			# Iterate through the list of MP3 files
			# Load each MP3 file
			audio = AudioSegment.from_mp3(mp3)

			# Combine the audio segments
			combined_audio += audio

			# Export the combined audio to the specified path
			combined_audio.export(speaker_path, format="mp3")



	input('Escape!')
	# raise Exception('ruh roh')
	# # # Word Level [Tonality between words is too different and doesn't flow well at all]
	# # TODO: create character limit for subtitles so it doesn't run offscreen
	# # # gather all paragraphs into unified list
	# wordtexts = []
	# wordstarts = []
	# wordends = []
	# cctexts = []
	# texts = []

	# # TODO: may need to have sentence timing because some words can persist on screen too long
	# # prefer to have sentences timing, but then ensure it's on the character limit
	# for word in words:
	# 	wordtexts.append(word['punctuated_word'])
	# 	wordstarts.append(word['start'])
	# 	wordends.append(word['end'])

	# # Initialization and limit definition
	# character_length = 50
	# i = 0
	# captionburn = ''
	# captionburnlist = []
	# startburnlist = [wordstarts[0]]
	# endburnlist = []

	# # TODO: figure out how to limit characters for translated language
	# while i<len(wordtexts): # Run until program has incremented through all words
	# 	captionburn = captionburn + str(wordtexts[i]) + ' ' + str(wordtexts[i+1]) + ' '
	# 	i+=2
	# 	if len(captionburn)>character_length: # Subtitle length limit
	# 		captionburnlist.append(captionburn[:-1]) # Add to subtitles list for voicing
	# 		try:
	# 			endburnlist.append(wordends[i-1])
	# 			startburnlist.append(wordstarts[i])
	# 		except:
	# 			print(captionburnlist, len(captionburnlist))
	# 			print(startburnlist,len(startburnlist))
	# 			print(endburnlist,len(endburnlist))
	# 		captionburn = '' # Reset captionburn variable for next phrase in list
	# 	if i+1 >= len(wordtexts): # Break condition when all words are captured
	# 		if wordtexts[-1] != wordtexts[i-1]: # Add stragler
	# 			captionburnlist.append(captionburn+str(wordtexts[-1]))
	# 		else:
	# 			captionburnlist.append(captionburn[:-1])
	# 		endburnlist.append(wordends[-1])
	# 		break

	# transcripts = captionburnlist
	# starts = startburnlist
	# ends = endburnlist

	end_time = time.time()
	transcribetime = end_time-start_time

# STEP #1.5: Translate transcription with a separate API for greater accuracy________________________________________
	# This step helps with word timing since Deepgram translations can be timed inconsistently
	start_time = time.time()
	if language != 'EN-US' and language != None:
		for transcript in transcripts:
			print(transcript)
			text = texttranslate(transcript, language)
			print(text)
			texts.append(text)
		print('Transcripts: ', transcripts)
		print('Texts: ', texts)
	elif language == None and captions:
		pass
	else:
		texts = transcripts

	end_time = time.time()
	translatetime = end_time-start_time

# STEP #2: Create sub-title file (if requested)______________________________________________________________________
	start_time = time.time()
	if captions:
		# Separate subtitle translation if caption language differ from voice
		if cclanguage != 'EN-US' and cclanguage != language:
			for transcript in transcripts:
				print(transcript)
				cctext = texttranslate(transcript, cclanguage)
				cctext = linebreak(cctext)
				print(cctext)
				cctexts.append(cctext)
		elif cclanguage == language:
			cctexts = texts
		elif cclanguage == 'EN-US':
			cctexts = transcripts
		elif cclanguage == None:
			pass
		else:
			raise Exception('tf?')
		
		# Create word-level subtitle file
		subtitles = convert_to_srtez(cctexts,starts,ends, path=filepath)
		subtitles = convert_that_ass(subtitles,filepath)
		# subtitles = convert_to_srt(subtitle_data, path=filepath) #TODO: make sure this works with new API
		# print('Subtitles created')
	else:
		subtitles = None
	end_time = time.time()
	captiontime = end_time-start_time

# STEP #3: Create AI voice__________________________________________________________________________________________
	aistart_time = time.time()
	if voice:
		info = subscriptioninfo()
		character_count = info['character_count']
		character_limit = info['character_limit']
		voices = {}
		# if character_count<character_limit:
		if True:
			print('New audio requested')

			# Use speaker voice if elected (always True currently)
			for speaker in range(speakercount+1):
				vocalspath = filepath+f'speaker{speaker}.mp3'
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
						voices[speaker] = voice['voice_id']
						print('Voice ID: ', voices[speaker])
						break

				# Voice added without upload error
				else:
					voices[speaker] = voice['voice_id']
					print(voice, type(voice))
			raise Exception('New territory that needs attention for new speakers')
			# Make ai voice for text
			i = 0
			for text in texts:
				# print(text)
				speaker = speakers[i]
				voice = voices[speaker]
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
	aiend_time = time.time()
	aivoicetime = aiend_time-aistart_time
# STEP #4: Combine AI vocals with background and add to video_______________________________________________________	
	# Combine background with AI voice:
	start_time = time.time()
	if captions and voice == False:
		pass
	else:
		overlay_audio(backgroundpath, new_audio, new_audio)

	# Add final audio to video file
	output_video = filepath+'jargonspeak_'+filename
	if subtitles != None and 'C:' in subtitles:
		subtitles = subtitles[49:] # issue with '/\' in FFMPEG; also should work on Heroku
	add_new_audio(filepath+filename, new_audio, subtitles, output_video)
	# print('New video file creation attempted')
	end_time = time.time()
	videocompiletime = end_time-start_time

# STEP #5: Cloud storage of video file______________________________________________________________________________
	# TODO: need to figure out permissions and link expiration; may be needed if filesize is too large to download
	start_time = time.time()
	mp4link = serverlink(output_video, 'jargonspeak_'+filename)
	if captions:
		srtlink = serverlink(filepath+'subtitles.srt', 'jargonspeak_'+'subtitles.srt')
	else:
		srtlink = None
	# jargonlink = None
	end_time = time.time()
	cloudtime = end_time-start_time

# STEP #6: Delete voice and remove files____________________________________________________________________________
	start_time = time.time()
	# Use glob to find all .wav files in the directory
	wav_files = glob.glob(os.path.join(filepath, "*.wav"))
	# Use glob to find all .mp4 files in the directory
	original_file = glob.glob(os.path.join(filepath, "original.mp4"))

	# Clear voice library space
	deletevoice(voice)

	# Iterate through the list of files and delete each one
	for wav_file in wav_files:
		os.remove(wav_file)
	# TODO: ERROR file still in use (subprocess.popen.(deletefiles)?)
	# for mp4_file in original_file:
	# 	os.remove(mp4_file)
	end_time = time.time()
	cleanuptime = end_time-start_time
	totalend = time.time()
	totaltime = totalend-totalstart
	timedictionary = {'splitaudiotime': f'{splitaudiotime}s', 'transcribetime': f'{transcribetime}s', 'translatetime': f'{translatetime}s', 'captiontime': f'{captiontime}s', 'aivoicetime': f'{aivoicetime}s', 'videocompiletime': f'{videocompiletime}s', 'cloudtime': f'{cloudtime}s', 'cleanuptime': f'{cleanuptime}s', 'totaltime': f"{totaltime}s"}
	print(timedictionary)
	return output_video, raw_text, mp4link, srtlink


if __name__ == '__main__':
	# # Julie's folder automation
	# filepath = r'C:\Users\clayt\Videos\Video Translation\Julie Translations\Originals/'
	# mp4_files = glob.glob(os.path.join(filepath, "*.mp4"))
	# for file in mp4_files:
	# 	filename = os.path.basename(file)
	# 	translatevideo(file, voice='Clone', captions=False, filepath=filepath, filename=filename, language='EN-US')

	# Other testing
	file = "C:/Users/clayt/Downloads/original.mp4"
	translatevideo(file, voice='Clone', captions=False, filepath='files/superuser/', filename='specialvideo.mp4', language='ES')
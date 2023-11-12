import subprocess
import time
import subprocess
import yt_dlp
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import AudioFileClip
import requests

def downloadvideo(url, local_filename):
	try:
		start = time.time()
		# Send a GET request to the URL
		response = requests.get(url, stream=True)
		response.raise_for_status()  # Check for any errors in the response

		# Open a local file for writing in binary mode
		with open(local_filename, 'wb') as local_file:
			for chunk in response.iter_content(chunk_size=8192):
				if chunk:  # Filter out keep-alive new chunks
					local_file.write(chunk)

		print(f"Downloaded {local_filename} successfully! ({round(time.time()-start,2)}s)")

	except Exception as e:
		print(f"An error occurred: {e}")
		# TODO: [video still downloads fine?] An error occurred: No connection adapters were found for 'C:\\Users\\clayt\\Documents\\Programming\\translait/files/croplex.mp4'


def crop(input_vid, output_vid, duration):
    start = time.time()
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', input_vid,
        '-ss', '0', '-t', duration, output_vid
    ]
    subprocess.run(ffmpeg_cmd)
    print(f"New audio/video created successfully! ({round(time.time()-start,2)}s)")

def split(input_vid, output_vid, start_time, end_time):
    start = time.time()
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', input_vid,
        '-ss', str(start_time), '-to', str(end_time),
		'-c:v', 'copy', '-c:a', 'copy', output_vid
    ]
    subprocess.run(ffmpeg_cmd)
    print(f"New audio/video created successfully! ({round(time.time()-start,2)}s)")

def youtubedownload(video, path):
	file = YouTube(video)
	stream = file.streams.filter(progressive=True).order_by('resolution').last() # first lowest, last highest
	print(stream)
	stream.download(filename=path)
	
def ytdownload(video_url, output):
    options = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_url])
        info_dict = ydl.extract_info(video_url, download=False)
        video_length = info_dict.get('duration', 0)

    return video_length

def ytvideolength(video_url):
    options = {
        'quiet': True,  # Suppress console output
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        video_length = info_dict.get('duration', 0)

    return video_length

def detectvideo(video, max_length, filepath, filename):
	# # Local file
	# if 'http' not in video:
	# 	# Get the duration of the video in seconds.
	# 	duration = VideoFileClip(video).duration
	# 	if duration < max_length:
	# 		downloadvideo(video, filepath+filename)
	# 	else:
	# 		raise Exception(f'Video length exceeds {max_length}s')

    # Youtube
	if 'youtube' in video or 'youtu.be' in video:
		print('YouTube video detected: ', video)

		# yt-dlp method (no age restriction, seemingly more reliable)
		duration = ytvideolength(video)
		if duration < max_length: 
			output = filepath+filename.strip()
			ytdownload(video, output)
			print('Video saved locally')

		# Pytube method
		# retries = 0
		# max_retries = 100
		# # Adding retry attempts because 503 and 403 exceptions occur randomly
		# while retries < max_retries:
		# 	# try:
		# 		file = YouTube(video) # use_oauth=True, allow_oauth_cache=True
		# 		duration = file.length
		# 		stream = file.streams.filter(progressive=True).order_by('resolution').last() # first lowest, last highest
		# 		if duration < max_length:
		# 			video = filepath+filename.strip()
		# 			# print(filename)
		# 			stream.download(filename=video)
		# 			print('Video saved locally')
		# 			break
		# 		else:
		# 			raise Exception(f'Video length exceeds {max_length}s')
		# 	# except: # TODO: if the exception is age restriction, then this is useless
		# 	# 	print(f'HTTP 503: Retrying ({retries + 1}/{max_retries})...')
		# 	# 	retries += 1

    # Audio files
	elif 'mp3' in video or 'wav' in video:
		try:
			print('Video url detected')
			duration = AudioFileClip(video).duration
		except Exception as e:
			return f"Error: {str(e)}"
		if duration < max_length:
			downloadvideo(video, filepath+filename)
		else:
			raise Exception(f'Video length exceeds {max_length}s')

    # Any other link
	else:
		try:
			print('Video url detected')
			duration = VideoFileClip(video).duration
		except Exception as e:
			return f"Error: {str(e)}"
		if duration < max_length:
			downloadvideo(video, filepath+filename)
		else:
			raise Exception(f'Video length exceeds {max_length}s')
	return duration

if __name__ == '__main__':
    # url = 'https://www.youtube.com/watch?v=E3-CpzZJl8w'
    # youtubedownload(url,'original.mp4')
    # crop('original.mp4','doordonot.mp4','59')
    # url = 'http://soundfxcenter.com/movies/star-wars/8d82b5_Lightsaber_Idle_Hum_Sound_Effect.mp3'
    # url = 'https://www.youtube.com/watch?v=Nn2H-XKEN98'
    # youtubedownload(url, 'jeffbooth.mp4')
	# url = 'https://d3ctxlq1ktw2nl.cloudfront.net/staging/2023-9-18/fdd10ffc-e065-c367-7ac2-a66b356837e6.mp3'
	# downloadvideo(url,'howtobuybitcoin.mp3')
	# duration = VideoFileClip('https://video.nostr.build/401b8475dc5aa523b2edc7fbeb462f09f168aac8f268a598ac3556aca279c7fa.mp4').duration
	# print(duration)
	# path = r'C:\Users\clayt\Documents\Programming\jargonspeak/files/f9ec6de472ec11eeba4418ff0f367121/'
	# split(path+'original.mp4',path+'crop.mp4',822,905)
	url = 'https://www.youtube.com/watch?v=Hd31dbJvGaU'
	length = ytdownload(url, 'natebargatze2.mp4')
	print(f'Video Length : {length}s')
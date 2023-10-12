import subprocess
import time
import subprocess
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
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


def youtubedownload(video, path):
	file = YouTube(video)
	stream = file.streams.filter(progressive=True).order_by('resolution').last() # first lowest, last highest
	print(stream)
	stream.download(filename=path)
	

def detectvideo(video, max_length, filepath, filename):
	# Local file
	if 'http' not in video:
		# Get the duration of the video in seconds.
		duration = VideoFileClip(video).duration
		if duration < max_length:
			downloadvideo(video, filepath+filename)
		else:
			raise Exception(f'Video length exceeds {max_length}s')

    # Youtube
	elif 'youtube' in video or 'youtu.be' in video:
		# If youtube
		print('YouTube video detected')
		file = YouTube(video)
		duration = file.length
		stream = file.streams.filter(progressive=True).order_by('resolution').last() # first lowest, last highest
		if duration < max_length:
			video = filepath+filename.strip()
			# print(filename)
			stream.download(filename=video)
			print('Video saved locally')
		else:
			raise Exception(f'Video length exceeds {max_length}s')

    # Any other link
	else:
		try:
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
    url = 'https://www.youtube.com/shorts/z8jgCkpdwd4'
    youtubedownload(url, 'video.mp4')
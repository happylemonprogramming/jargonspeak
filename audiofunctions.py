from pydub import AudioSegment
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import AudioFileClip, concatenate_audioclips
import subprocess
import os
import time

def addsilence(input,output, duration):
    start = time.time()
    # Load the original MP3 file
    audio = AudioSegment.from_file(input, format="mp3") #wav does not work for some reason even though it seems to work in other functions

    # Generate a silence audio segment
    silence = AudioSegment.silent(duration=duration)

    # Add silence before or after the audio
    audio_with_silence_before = silence + audio
    # Alternatively, to add silence after the audio: audio_with_silence_after = audio + silence

    # Export the audio with added silence as an MP3 file
    audio_with_silence_before.export(output, format="mp3")
    print(f"Silence added successfully! ({round(time.time()-start,2)}s)")

def overlay_audio(file1, file2, output_path):
    start = time.time()
    audio1 = AudioSegment.from_file(file1)
    audio2 = AudioSegment.from_file(file2)
    combined = audio1.overlay(audio2)
    combined.export(output_path, format="wav")
    print(f"Audio overlayed successfully! ({round(time.time()-start,2)}s)")
    return output_path

def reduceaudiovolume(input_file, output_file, volume):
    start = time.time()
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Reduce the volume by X% (adjust as needed)
    reduced_volume_audio = audio + (audio.dBFS * volume)
    # print(reduced_volume_audio)
    # Export the adjusted audio
    reduced_volume_audio.export(output_file, format="wav")
    print(f"Audio level reduced successfully! ({round(time.time()-start,2)}s)")

def extract_audio(mp4_filename, audio_filename='videovoice.wav'):
    start = time.time()
    video_clip = VideoFileClip(mp4_filename)
    audio_clip = video_clip.audio

    audio_clip.write_audiofile(audio_filename)
    audio_clip.close()
    print(f"Audio extracted successfully! ({round(time.time()-start,2)}s)")

def audioslicing(video_url, start, end):
    # Load the video clip
    video_clip = VideoFileClip(video_url)

    # Extract audio from the video clip
    audio = video_clip.audio

    # Export the audio to a temporary WAV file
    temp_audio_file = "temp_audio.wav"
    audio.write_audiofile(temp_audio_file)

    try:
        # Convert audio to AudioSegment for slicing
        audio_segment = AudioSegment.from_file(temp_audio_file)

        # Slice the audio segment
        sliced_audio = audio_segment[start:end]

        # Export sliced audio to the specified output filename
        output = 'audioslice.wav'
        sliced_audio.export(output, format='wav')
    finally:
        # Clean up: delete the temporary audio file
        os.remove(temp_audio_file)
    return output


def audiocombine(path1,path2):
    # Load audio clips
    clip1 = AudioFileClip(path1)
    clip2 = AudioFileClip(path2)

    # Concatenate audio clips
    concatenated_clip = concatenate_audioclips([clip1, clip2])

    # Export the concatenated clip
    output = 'concatenated_audio.wav'
    concatenated_clip.write_audiofile(output)
    return output

def add_new_audio(input_video, new_audio=None, subtitles=None, output_video='output.mp4'):
    start = time.time()
    if subtitles == None and new_audio != None:
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', input_video,
            '-i', new_audio,
            # '-vf', f'subtitles={subtitles}',
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
            '-c:a', 'aac', '-b:a', '192k',  # You can adjust the audio codec and bitrate as needed
            '-map', '0:v', '-map', '1:a',
            '-y', output_video
        ]
    elif new_audio == None and subtitles != None:
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', input_video,
            # '-i', new_audio,
            '-vf', f'subtitles={subtitles}',
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
            '-c:a', 'aac', '-b:a', '192k',  # You can adjust the audio codec and bitrate as needed
            # '-map', '0:v', '-map', '1:a',
            '-y', output_video
        ]

    else:
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', input_video,
            '-i', new_audio,
            '-vf', f'subtitles={subtitles}',
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
            '-c:a', 'aac', '-b:a', '192k',  # You can adjust the audio codec and bitrate as needed
            '-map', '0:v', '-map', '1:a',
            '-y', output_video
        ]
    subprocess.run(ffmpeg_cmd)
    print(f"New audio/video created successfully! ({round(time.time()-start,2)}s)")

def audiospeed(input_audio, output_audio, speed):
    start = time.time()
    if speed <= 1.00:
        speed = 1.00
    else:
        speed = speed
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', input_audio,
        '-filter:a',
        f'atempo={speed}', output_audio
    ]
    subprocess.run(ffmpeg_cmd)
    print(f"New audio/video created successfully! ({round(time.time()-start,2)}s)")

def separateaudio(file):
    # Define the command to execute
    command = f"spleeter separate -p spleeter:2stems -o output {file}"

    # Use subprocess to run the command
    try:
        subprocess.run(command)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # path = r'files\10.wav'
    # speed = 1.5
    # output = 'superfile.wav'

    # speedchange(path)
    # speed_change(path, speed_factor=2.0)
    # speed_up_audio(path, output, speed_factor=speed)
    # audiospeed(path, output, speed)
    separateaudio(r"C:\Users\clayt\Documents\Programming\translait\files\asfdasdf.mp4")
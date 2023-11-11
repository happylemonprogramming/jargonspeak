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
    print('Extract Audio response: ', video_clip) # debug
    audio_clip = video_clip.audio

    audio_clip.write_audiofile(audio_filename)
    audio_clip.close()
    print(f"Audio extracted successfully! ({round(time.time()-start,2)}s)")

def audioslicing(video_url, start, end, output = 'audioslice.mp3'):
    if 'http' in video_url:
        # Load the video clip
        video_clip = VideoFileClip(video_url)

        # Extract audio from the video clip
        audio = video_clip.audio
    else:
        audio = AudioFileClip(video_url)

    # Export the audio to a temporary WAV file
    temp_audio_file = "temp_audio.wav"
    audio.write_audiofile(temp_audio_file)

    try:
        # Convert audio to AudioSegment for slicing
        audio_segment = AudioSegment.from_file(temp_audio_file)

        # Convert to milliseconds from seconds
        start = start*1000
        end = end*1000
        # Slice the audio segment
        sliced_audio = audio_segment[start:end]

        # Export sliced audio to the specified output filename
        sliced_audio.export(output, format='mp3')
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

# import base64

# # Read the font file as binary
# with open('fonts/YuGothR.ttc', 'rb') as font_file:
#     font_data = font_file.read()

# # Encode the font file as base64
# encoded_font = base64.b64encode(font_data).decode('utf-8')

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
            '-vf', f"subtitles={subtitles}", # :force_style='FontName=fonts/NotoSansJP-Regular.ttf'
            # '-vf', f"subtitles={subtitles}:force_style='FontName=DejaVu Serif,Fontsize=24'",
            # '-vf', f"subtitles=subtitle_file.srt:force_style='FontName=data:font/truetype;charset=utf-8;base64,{encoded_font},FontSize=24'",
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
            '-vf', f"subtitles={subtitles}", # :force_style='FontName=fonts/NotoSansJP-Regular.ttf'
            # '-vf', f"subtitles={subtitles}:force_style='FontName=DejaVu Serif,Fontsize=24'",
            # '-vf', f"subtitles=subtitle_file.srt:force_style='FontName=data:font/truetype;charset=utf-8;base64,{encoded_font},FontSize=24'",
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
            '-c:a', 'aac', '-b:a', '192k',  # You can adjust the audio codec and bitrate as needed
            '-map', '0:v', '-map', '1:a',
            '-y', output_video
        ]
    subprocess.run(ffmpeg_cmd)
    print(f"New audio/video created successfully! ({round(time.time()-start,2)}s)")

def audiospeed(input_audio, output_audio, speed):
    start = time.time()
    # Speed is bounded by limits of FFMPEG [0.50,100.00]
    if speed < 0.66: # Below 2/3X speed, speech is too stretched (Tradeoff: there will be a pause)
        speed = 0.66
    elif speed > 3.00: # Beyond 3X speed, speech is unintelligible (Tradeoff: potential overlapping)
        speed = 3.00
    else:
        speed = speed
    ffmpeg_cmd = [
        'ffmpeg',
        '-y',
        '-i', input_audio,
        '-filter:a',
        f'atempo={speed}', output_audio
    ]
    subprocess.run(ffmpeg_cmd)
    print(f"New audio speed created successfully! ({round(time.time()-start,2)}s)")

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
    # separateaudio(r"C:\Users\clayt\Documents\Programming\translait\files\asfdasdf.mp4")
    # original_path = r'C:\Users\clayt\Videos\Video Translation\Julie Translations\Test\RPReplay_Final1695273035.MP4'
    # new_audio_path = r"C:\Users\clayt\Videos\Video Translation\Julie Translations\Test\51.wav"
    # filename = os.path.basename(original_path)
    # add_new_audio(input_video=original_path,new_audio=new_audio_path,subtitles=None,output_video=f'jargonspeak_{filename}')
    # file = r'C:\Users\clayt\Documents\Programming\jargonspeak\files\77dd48b86c7911eeaf4f18ff0f367121\extractedaudio.mp3'
    # audiospeed(file,'slow.mp3',0.60)
    # file = r'C:\Users\clayt\Documents\Programming\jargonspeak\bitcoin_audible10.wav'
    # audioslicing(file, 0,58000)
    file = r'C:\Users\clayt\Documents\Programming\jargonspeak\micorazon.mp4'
    extract_audio(file,'corazonaudio.mp3')
    
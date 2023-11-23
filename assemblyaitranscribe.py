import requests
import json
import time
import os

def assemblytranscribe(path):
  base_url = "https://api.assemblyai.com/v2"

  headers = {
      "authorization": os.environ['assemblyaiapikey']
  }

  with open(path, "rb") as f:
    response = requests.post(base_url + "/upload",
                            headers=headers,
                            data=f)

  upload_url = response.json()["upload_url"]

  data = {
      "audio_url": upload_url # You can also use a URL to an audio or video file on the web
      # "speaker_labels": True,
      # "speakers_expected": 2
  }

  url = base_url + "/transcript"
  response = requests.post(url, json=data, headers=headers)
  print(response.text)
  transcript_id = response.json()['id']
  polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

  while True:
    transcription_result = requests.get(polling_endpoint, headers=headers).json()

    if transcription_result['status'] == 'completed':
      with open('assemblyresult2.txt', 'w', encoding='utf-8') as file:
        file.write(str(transcription_result))
      break

    elif transcription_result['status'] == 'error':
      raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

    else:
      time.sleep(3)
      print('sleepy')

if __name__ == '__main__':
  other_path = r"C:\Users\clayt\Videos\AI Story Teller Movies\father son travel to mars on rocketship.mp4"
  path = "C:/Users/clayt/Videos/Video Translation/Julie Translations/To Be Translated/RPReplay_Final1695652113.MP4"
  assemblytranscribe(path)
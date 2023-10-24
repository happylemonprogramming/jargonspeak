import requests
import json
import time
import os

api_key = os.environ['moisesaiapikey']

# Requesting signed URLs
def requestupload():
    url = "https://developer-api.moises.ai/api/upload"
    headers = {
        "Authorization": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Moises audio upload request successful.")
        output = response.json()
        uploadUrl = output['uploadUrl']
        downloadUrl = output['downloadUrl']

    else:
        print(f"Moises audio upload request failed with status code {response.status_code}.")
        print("Response content:")
        print(response.text)
        uploadUrl, downloadUrl = None
    return uploadUrl, downloadUrl

# Upload a file
def uploadfile(uploadUrl, filepath, filename='track.mp3'):
    files = {'filedata': (filename, open(filepath, 'rb'), 'multipart/form-data')}

    response = requests.put(uploadUrl, files=files)

    if response.status_code == 200:
        print("Moises audio file successfully uploaded.")
    else:
        print(f"Moises failed to upload file. Status code: {response.status_code}")
        print(response.text)

# Generate Job ID
def createjob(name, downloadUrl):
    url = "https://developer-api.moises.ai/api/job"

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    data = {
        "name": name,
        "workflow": "moises/stems-vocals-accompaniment",
        "params": {
            "inputUrl": downloadUrl
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Moises job created successfully.")
        job_id = response.json().get("id")
        print(f"Job ID: {job_id}")
    else:
        print(f"Moises failed to create job. Status code: {response.status_code}")
        print(response.text)
        job_id = None
    return job_id

def getjobstatus(job_id):
    url = f"https://developer-api.moises.ai/api/job/{job_id}"

    headers = {
        "Authorization": api_key
    }

    response = requests.get(url, headers=headers)
    status = None
    vocals = None
    background = None
    if response.status_code == 200:
        print("Moises status request was successful.")
        data = response.json()  # Parse the JSON response
        status = data['status']
        if data['result'] != {}:
            vocals = data['result']['vocals']
            background = data['result']['accompaniment']
    else:
        print(f"Request failed. Status code: {response.status_code}")
        print(response)
    return status, vocals, background

def deletejob(job_id):
    url = f"https://developer-api.moises.ai/api/job/{job_id}"

    headers = {
        "Authorization": api_key
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print("Moises delete request was successful. The resource has been deleted.")
        print(response)
    else:
        print(f"Moises delete request failed. Status code: {response.status_code}")
        print(response)

def splitaudio(audio):
    uploadUrl, downloadUrl = requestupload()
    uploadfile(uploadUrl, audio)
    job_id = createjob('jargonspeak', downloadUrl)
    status = getjobstatus(job_id)[0]
    # Default values
    vocals = None
    background = None
    print('Job status: ', status)
    while status != 'SUCCEEDED' or status != 'FAILED':
        time.sleep(1)
        status = getjobstatus(job_id)[0]
        print('Job status: ', status)
        if status == 'SUCCEEDED':
            status, vocals, background = getjobstatus(job_id)
            print('Split complete.')
            break
        elif status == 'FAILED' or status == None:
            raise Exception(f'Split failed.')
        else:
            print('Audio split in progress...')
    return vocals, background

if __name__ == '__main__':
    # uploadUrl, downloadUrl = requestupload()
    # uploadfile(uploadUrl, 'videovoice.mp3', 'input.')
    # job_id = createjob('Ye Job', downloadUrl)
    # job_id = 'd7ee2889-20a3-472f-8bc9-3d1eadd41213'
    # print(getjobstatus(job_id))
    # vocals, background = splitaudio('videovoice.mp3')
    # print(vocals)
    # print(background)
    print(splitaudio(r'C:\Users\clayt\Documents\Programming\jargonspeak\files\9d5b8a9b6fde11ee97d118ff0f367121\extractedaudio.mp3'))
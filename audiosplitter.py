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
        print("Request was successful.")
        output = response.json()
        uploadUrl = output['uploadUrl']
        downloadUrl = output['downloadUrl']

    else:
        print(f"Request failed with status code {response.status_code}.")
        print("Response content:")
        print(response.text)
        uploadUrl, downloadUrl = None
    return uploadUrl, downloadUrl

# Upload a file
def uploadfile(uploadUrl, filepath, filename='track.mp3'):
    files = {'filedata': (filename, open(filepath, 'rb'), 'multipart/form-data')}

    response = requests.put(uploadUrl, files=files)

    if response.status_code == 200:
        print("File successfully uploaded.")
        print(response)
    else:
        print(f"Failed to upload file. Status code: {response.status_code}")
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
        print("Job created successfully.")
        print(response.text)
        job_id = response.json().get("id")
        print(f"Job ID: {job_id}")
    else:
        print(f"Failed to create job. Status code: {response.status_code}")
        print(response.text)
        job_id = None
    return job_id

def getjobstatus(job_id):
    url = f"https://developer-api.moises.ai/api/job/{job_id}"

    headers = {
        "Authorization": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Request was successful.")
        data = response.json()  # Parse the JSON response
        print("getjobstatus:", data)
        status = data['status']
        if data['result'] != {}:
            vocals = data['result']['vocals']
            background = data['result']['accompaniment']
        else:
            vocals = None
            background = None
    else:
        vocals = None
        background = None
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
        print("Request was successful. The resource has been deleted.")
        print(response)
    else:
        print(f"Request failed. Status code: {response.status_code}")
        print(response)

def splitaudio(audio):
    uploadUrl, downloadUrl = requestupload()
    uploadfile(uploadUrl, audio)
    job_id = createjob('jargonspeak', downloadUrl)
    status = getjobstatus(job_id)[0]
    while status == 'STARTED':
        time.sleep(1)
        status = getjobstatus(job_id)[0]
        if status == 'SUCCEEDED':
            status, vocals, background = getjobstatus(job_id)
            print('Split complete.')
            break
        elif status == 'FAILED':
            print('Split failed.')
            raise FileNotFoundError()
        print('Audio split in progress...')
    return vocals, background

if __name__ == '__main__':
    # uploadUrl, downloadUrl = requestupload()
    # uploadfile(uploadUrl, 'videovoice.mp3', 'input.')
    # job_id = createjob('Ye Job', downloadUrl)
    # job_id = '2001316e-835c-4fe2-9c15-f61a658d4c00'
    # getjobstatus(job_id)
    vocals, background = splitaudio('videovoice.mp3')
    print(vocals)
    print(background)
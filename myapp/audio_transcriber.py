import requests, time, os
from dotenv import load_dotenv

load_dotenv()
apiKey = os.getenv("transcribeAPIKey")
baseUrl = "https://api.assemblyai.com"
headers = {"authorization": apiKey}
#
#Uploads audio file to AssemblyAI
#
def transcribeAudio(video_file):
    response = requests.post(baseUrl + "/v2/upload", headers=headers, data=video_file)
    if response.status_code != 200:
        print(f"Error: {response.status_code}, Response: {response.text}")
        response.raise_for_status()
        return "Error"
    upload_json =  response.json()
    upload_url = upload_json["upload_url"]
    data = {"audio_url": upload_url, "speech_model": "slam-1"}

    response = requests.post(baseUrl + "/v2/transcript", headers=headers, json=data)
    if response.status_code != 200:
        print(f"Error: {response.status_code}, Response: {response.text}")
        response.raise_for_status()
        return "Error"

    transcriptionId = response.json()["id"]
    transcriptJson = response.json()
    pollingEndpoint = f"{baseUrl}/v2/transcript/{transcriptionId}"

    while True:
        transcript = requests.get(pollingEndpoint, headers=headers).json()
        if transcript["status"] == "completed":
            return transcript["text"]
        elif transcript["status"] != "error":
            print("waiting..")
            time.sleep(2)
        else:
            print(f"Error: {transcript['error']}")
            return "Error"



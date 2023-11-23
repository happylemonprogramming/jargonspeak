import requests
import os

# Set your API key and image file path
api_key = os.environ['clipdropapikey']

def removetext(inputImage, outputImage='noTextImage.png'):
  # API endpoint URL
  url = 'https://clipdrop-api.co/remove-text/v1'

  # Set the headers with the API key
  headers = {'x-api-key': api_key}

  # Prepare the files for the POST request
  files = {'image_file': open(inputImage, 'rb')}

  # Make the POST request
  response = requests.post(url, headers=headers, files=files)

  # Check if the request was successful (status code 200)
  if response.status_code == 200:
      # Save the response content to the output file
      with open(outputImage, 'wb') as output_file:
          output_file.write(response.content)
      print(f"Text removed successfully. Result saved to {outputImage}")
  else:
      # Print an error message if the request was not successful
      print(f"Error: {response.status_code} - {response.text}")

if __name__ == '__main__':
  image_file_path = r"C:\Users\clayt\Pictures\Screenshots\Screenshot 2023-03-26 231819.png"
  output_file_path = 'result.png'
  removetext(image_file_path,output_file_path)
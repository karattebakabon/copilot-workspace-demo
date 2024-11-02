import requests
import os
import shutil

def download_media(tumblr_id):
    # Create a folder with the Tumblr ID name
    if not os.path.exists(tumblr_id):
        os.makedirs(tumblr_id)

    # Define the URL for the Tumblr API
    api_url = f"https://{tumblr_id}.tumblr.com/api/read/json"

    # Send a request to the Tumblr API
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for {tumblr_id}")
        return

    # Parse the JSON response
    data = response.json()

    # Iterate through the posts and download images and videos
    for post in data['posts']:
        if 'photo-url-1280' in post:
            media_url = post['photo-url-1280']
            media_type = 'image'
        elif 'video-player' in post:
            media_url = post['video-player']
            media_type = 'video'
        else:
            continue

        # Extract the file name from the URL
        file_name = media_url.split('/')[-1]
        file_path = os.path.join(tumblr_id, file_name)

        # Skip downloading if the file already exists
        if os.path.exists(file_path):
            print(f"Skipping {file_name}, already exists.")
            continue

        # Download the media file
        media_response = requests.get(media_url, stream=True)
        if media_response.status_code == 200:
            with open(file_path, 'wb') as file:
                shutil.copyfileobj(media_response.raw, file)
            print(f"Downloaded {file_name}")
        else:
            print(f"Failed to download {file_name}")

if __name__ == "__main__":
    tumblr_id = input("Enter the Tumblr ID: ")
    download_media(tumblr_id)

'''Uploads file to Amazon AWS (S3) and returns authorized link'''

import os
import boto3
import time

# Environment variables
awssecret = os.environ["AWS_SECRET_ACCESS_KEY"]
awsaccess = os.environ["AWS_ACCESS_KEY_ID"]

def serverlink(local_filepath, object_name='video.mp4'):
    start = time.time()
    # Create an S3 client
    s3 = boto3.client('s3')

    filename = local_filepath  # This is the local file that you want to upload
    bucket_name = 'privatevideotranslation'  # The name of your S3 bucket
    # object_name = 'testvideo.mp4'  # The name you want the file to have on S3
    region = 'us-west-1' # Region where the server resides

    # Uploads the given file using a managed uploader, which will split up large
    # files automatically and upload parts in parallel.
    s3.upload_file(filename, bucket_name, object_name, ExtraArgs={'ContentType': "video/mp4"})

    # Create Url
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name,
            'Key': object_name,
            'ResponseContentDisposition': f'attachment; filename="{object_name}"' if object_name else 'attachment'
        },
        ExpiresIn=24*60*60
    )

    print(f"Uploaded {object_name} successfully! ({round(time.time()-start,2)}s)")

    return url

if __name__ == "__main__":
    path = r"C:\Users\clayt\Videos\Video Translation\Guy Swan Translation\original.mp4"
    name = 'guy.mp4'
    print(serverlink(path,name))
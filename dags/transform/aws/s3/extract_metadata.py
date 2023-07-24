import boto3
import exiftool
import tempfile
from pprint import pprint

import pandas as pd
import os



AWS_ACCESS_KEY = os.getenv("AAA_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AAA_SECRET_ACCESS_KEY")

BUCKET_NAME_METADATA = "metadatabucketttt"
BUCKET_NAME_IMAGE = "newimagebuckettest"

def extract_metadata_s3(photo_name):
    s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY,
                      )

    # Create a temporary file to save the downloaded image
    with tempfile.NamedTemporaryFile() as temp_file:
        print(f'here is photo_name = {photo_name}')
        print(f'here is temp_file.name = {temp_file.name}')
        # Download the image from S3 to the temporary file
        s3.download_file(BUCKET_NAME_IMAGE, photo_name, temp_file.name)

        # Use pyexiftool to extract metadata from the downloaded image file
        with exiftool.ExifToolHelper() as et:
            metadata = et.get_metadata(temp_file.name)
            metadata = metadata[0]

            result_data = {"ImageSize": metadata.get("Composite:ImageSize"),
                           "FileType": metadata.get("File:FileType"),
                           "MIMEType": metadata.get("File:MIMEType"),
                           "BitsPerSample": metadata.get("File:BitsPerSample"),
                           "ProfileClass": metadata.get("ICC_Profile:ProfileClass"),
                           "RenderingIntent": metadata.get("ICC_Profile:RenderingIntent"),
                           "CreateDate": metadata.get("XMP:CreateDate")\
                           }
            """
            result_data = [metadata.get("Composite:ImageSize"),
                            metadata.get("File:FileType"),
                           metadata.get("File:MIMEType"),
                           metadata.get("File:BitsPerSample"),
                           metadata.get("ICC_Profile:ProfileClass"),
                           metadata.get("ICC_Profile:RenderingIntent"),
                           metadata.get("XMP:CreateDate")
                           ]
            """



    """
    Composite:ImageSize
    File:FileType
    File:MIMEType
    File:BitsPerSample
    ICC_Profile:ProfileClass
    ICC_Profile:RenderingIntent
    XMP:CreateDate
    """
    #return metadata
    return result_data

# Example usage



"""

def main():
    photo_name = "FLICKR-dogs-0fe3350239cd46e99dca35f5ecda5973.png"
    result = extract_metadata_s3(photo_name=photo_name)
    pprint(result)


if __name__ == '__main__':
    main()
"""
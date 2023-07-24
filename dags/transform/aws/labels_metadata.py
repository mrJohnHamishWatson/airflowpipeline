# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)
import os
from typing import List

import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AAA_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AAA_SECRET_ACCESS_KEY")

BUCKET_NAME_METADATA = "metadatabucketttt"
BUCKET_NAME_IMAGE = "newimagebuckettest"


def detect_labels(photo: str) -> List or str:
    #try:
        result_list = []
    # session = boto3.Session(profile_name='profile-name')
    # client = session.client('rekognition')
        client = boto3.client(
            "rekognition",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name='us-east-1'
        )
        response = client.detect_labels(
        Image={"S3Object": {"Bucket": BUCKET_NAME_IMAGE, "Name": photo}}
        # MaxLabels=10,
        # Uncomment to use image properties and filtration settings
        # Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"],
        # Settings={"GeneralLabels": {"LabelInclusionFilters":["Cat"]},
        # "ImageProperties": {"MaxDominantColors":10}}
        )
        print()
        print(response)
        labels = response.get("Labels")
        if not labels:
            return "NONE"

        for label in labels:
            result_list.append(label["Name"])
            print("Label: " + label["Name"])
            print("Confidence: " + str(label["Confidence"]))
            print("Instances:")
            instances = label.get("Instances")
            #if not instances:
            #    return "NONE"
            if instances:

                for instance in instances:
                    print(" Bounding box")
                    print(" Top: " + str(instance["BoundingBox"]["Top"]))
                    print(" Left: " + str(instance["BoundingBox"]["Left"]))
                    print(" Width: " + str(instance["BoundingBox"]["Width"]))
                    print(" Height: " + str(instance["BoundingBox"]["Height"]))
                    print(" Confidence: " + str(instance["Confidence"]))
                    print()

            print("Parents:")
            parents = label.get("Parents")
            #if not parents:
            #    return "NONE"
            if parents:
                for parent in parents:
                    print(" " + parent["Name"])
                    result_list.append(parent["Name"])

            print("Aliases:")
            aliases = label.get("Aliases")
            if aliases:
                for alias in label.get("Aliases"):
                    print(" " + alias["Name"])
                    result_list.append(alias["Name"])

                    print("Categories:")
            categories = label.get("Categories")
            #if not categories:
            #    return "NONE"
            if categories:
                for category in categories:
                    print(" " + category["Name"])
                    result_list.append(category["Name"])
                    print("----------")
                    print()

        if "ImageProperties" in str(response):
            print("Background:")
            print(response["ImageProperties"]["Background"])
            print()
            print("Foreground:")
            print(response["ImageProperties"]["Foreground"])
            print()
            print("Quality:")
            print(response["ImageProperties"]["Quality"])
            print()

    # return len(response["Labels"])
        return result_list
    #except Exception as err:
    #    print(f"here is error: ")
    #    print(err)
    #    print(f'error in image = {photo}')
    #    return "NONE"


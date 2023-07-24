import os
from datetime import datetime
from typing import List

import boto3
import click
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from dotenv import load_dotenv
from io import StringIO

from aws.labels_metadata import detect_labels
from aws.s3.extract_metadata import extract_metadata_s3

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AAA_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AAA_SECRET_ACCESS_KEY")

BUCKET_NAME_METADATA = "metadatabucketttt"
BUCKET_NAME_IMAGE = "newimagebuckettest"


def get_s3_files(s3) -> List:
    response = s3.list_objects_v2(Bucket=BUCKET_NAME_METADATA)

    # Проверка наличия файлов в ведре
    if "Contents" in response:
        # Извлечение списка файлов
        objects = response["Contents"]

        # Печать имен файлов
        data = [obj["Key"] for obj in objects if ".json" in obj["Key"]]
        return data
    else:
        print("Ведро S3 пустое.")


def get_data_from_s3(s3, key):
    print(f"BUCKET_NAME_METADATA = {BUCKET_NAME_METADATA}")
    print(f"key = {key}")

    # Загрузка JSON-файла из S3
    response = s3.get_object(Bucket=BUCKET_NAME_METADATA, Key=key)
    return response["Body"].read().decode("utf-8")


def get_json_from_s3(s3, key):
    data = get_data_from_s3(s3=s3, key=key)
    print(f"data = {data}")
    string_data = StringIO(data)
    print(f"string_data = {string_data}")
    print()
    print()
    print()
    df = pd.read_json(string_data)
    return df


def get_tags_df(df):
    df["tags"] = df["file_name"].apply(detect_labels)
    return df


def drop_none_tag(df):
    return df[~(df["tags"] == "NONE")]


def get_metadata_df(df):
    try:
        df[
        [
            "ImageSize",
            "FileType",
            "MIMEType",
            "BitsPerSample",
            "ProfileClass",
            "RenderingIntent",
            "CreateDate",
        ]
        ] = df["file_name"].apply(lambda x: pd.Series(extract_metadata_s3(x)))
    except Exception as err:
        print(err)
    return df


def _write_parquet_file(df) -> str:
    table = pa.Table.from_pandas(df)
    time_now = datetime.now().strftime("%Y-%m-%d%-H-%M-%S")

    parquet_name = f"data{time_now}.parquet"
    pq.write_table(table, parquet_name)
    return parquet_name


def send_s3_parquet(parquet_name: str):
    # Подключаемся к S3
    s3 = boto3.resource("s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

    # Загружаем файл на S3
    s3.Bucket(BUCKET_NAME_METADATA).upload_file(parquet_name, f"silver/{parquet_name}")


def save_file(df):
    parquet_name = _write_parquet_file(df)
    send_s3_parquet(parquet_name)
    os.remove(parquet_name)


def process_file(filename: str, s3):
    df = get_json_from_s3(s3=s3, key=filename)

    print(df)
    df = get_tags_df(df)

    print(df)
    df = drop_none_tag(df)

    df = get_metadata_df(df)

    print(df)
    save_file(df)



@click.group()
def cli():
    pass


@cli.command(name="transform")
def transform_data():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )
    list_files = get_s3_files(s3)
    print(list_files)

    for file in list_files:
        process_file(file, s3)



def main():
    cli()


if __name__ == '__main__':
    main()

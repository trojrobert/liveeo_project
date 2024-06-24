from prefect import task, Flow
import boto3
import requests
import snowflake.connector
import json

s3_client = boto3.client("s3")
bucket_name = "my-s3-bucket"


@task
def upload_images_to_s3_task(stac_item):
    assets = stac_item["assets"]
    for asset_key, asset in assets.items():
        if asset["type"].startswith("image/"):
            image_url = asset["href"]
            image_response = requests.get(image_url, stream=True)
            image_response.raise_for_status()
            s3_key = f"stac_assets/{stac_item['id']}/{asset_key}.tif"
            s3_client.upload_fileobj(image_response.raw, bucket_name, s3_key)
            asset["s3_href"] = f"s3://{bucket_name}/{s3_key}"
    return stac_item


@task
def upload_metadata_to_snowflake_task(stac_item):
    conn = snowflake.connector.connect(
        user="your_user", password="your_password", account="your_account"
    )
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO stac_metadata.stac_items (id, item_metadata, geometry)
        VALUES (%s, PARSE_JSON(%s), GEOGRAPHY::ST_GeomFromGeoJSON(%s))
    """
    cursor.execute(
        insert_query,
        (stac_item["id"], json.dumps(stac_item), json.dumps(stac_item["geometry"])),
    )
    conn.commit()
    cursor.close()
    conn.close()


@flow
def upload_data_flow():
    upload_images_to_s3_task()
    upload_metadata_to_snowflake_task()


if "__name__" == "__main__":
    upload_data_flow()

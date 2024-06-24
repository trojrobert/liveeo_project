import cv2
import numpy as np
import boto3


s3 = boto3.client("s3")


@task
def disparity_matching_task(stac_item):
    left_image_s3_url = stac_item["assets"]["left"]["s3_href"]
    right_image_s3_url = stac_item["assets"]["right"]["s3_href"]

    # Download images from S3
    left_image = download_image_from_s3(left_image_s3_url)
    right_image = download_image_from_s3(right_image_s3_url)

    # Perform disparity matching (example using OpenCV's StereoBM)
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(left_image, right_image)

    return disparity


def download_image_from_s3(s3_url):
    bucket, key = parse_s3_url(s3_url)
    obj = s3.get_object(Bucket=bucket, Key=key)
    img = np.asarray(bytearray(obj["Body"].read()), dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_GRAYSCALE)
    return img


def parse_s3_url(s3_url):
    parts = s3_url.replace("s3://", "").split("/", 1)
    return parts[0], parts[1]


@flow
def disparity_matching_flow():
    disparity = disparity_matching_task()


if "__name__" == "__main__":
    disparity_matching_flow()

@task
def save_results_to_s3_task(stac_item, corrected_disparity):
    s3_key = f"processed_assets/{stac_item['id']}/corrected_disparity.tif"
    s3_client.put_object(
        Body=corrected_disparity.tobytes(), Bucket=bucket_name, Key=s3_key
    )
    update_snowflake_with_results(stac_item["id"], s3_key)


@task
def update_snowflake_with_results_task(item_id, s3_key):
    conn = snowflake.connector.connect(
        user="your_user", password="your_password", account="your_account"
    )
    cursor = conn.cursor()
    update_query = """
        UPDATE stac_metadata.stac_items
        SET processed_data_s3_key = %s
        WHERE id = %s
    """
    cursor.execute(update_query, (s3_key, item_id))
    conn.commit()
    cursor.close()
    conn.close()


@flow
def update_result_flow():
    save_results_to_s3_task()
    update_snowflake_with_results_task()


if "__name__" == "__main__":
    update_result_flow()

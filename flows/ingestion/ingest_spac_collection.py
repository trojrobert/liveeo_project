from pystac_client import Client
from prefect import task, flow


@task
def fetch_stac_collection_task():
    # Open the STAC client to connect to the Earth Search catalog
    client = Client.open("https://earth-search.aws.element84.com/v1")

    # Perform a search for Sentinel-2 L2A imagery within the specified bounding box
    search = client.search(
        max_items=10, collections=["sentinel-2-l2a"], bbox=[-72.5, 40.5, -72, 41]
    )

    # Convert the search results to a dictionary
    search_results = search.item_collection_as_dict()

    # Check if any results are found
    if not search_results["features"]:
        raise ValueError("No search results found")

    return search_results["features"]


@flow
def ingest_spac_collection_flow():
    stac_collection = fetch_stac_collection_task()


if "__main__" == "__name__":
    ingest_spac_collection_flow()

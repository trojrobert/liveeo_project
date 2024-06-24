from platform import node, platform, python_version
import prefect
from prefect import flow, get_run_logger


@flow
def maintenance():
    "This function shows the python verison and check for healthy network"
    version = prefect.__version__
    logger = get_run_logger()
    logger.info("Network: %s. Instance: %s. Agent is healthy ✅️", node(), platform())
    logger.info("Python = %s. Prefect = %s 🚀", python_version(), version)


if __name__ == "__main__":
    maintenance()

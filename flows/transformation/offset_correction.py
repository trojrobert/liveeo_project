import numpy as np


@task
def offset_correction_task(disparity):
    offset_corrected = disparity - np.mean(disparity)
    return offset_corrected


@flow
def offset_correction_flow():
    offset_corrected = offset_correction()


if "__name__" == "__main__":
    offset_correction_flow()

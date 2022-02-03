import logging

import azure.functions as func
from ecgai_training_data_physionet.ptbxl import PtbXl


async def get_record(record_id: int) -> func.HttpResponse:
    try:
        physionet_data = PtbXl(data_location='data')
        record_task = physionet_data.get_record(record_id=record_id)
        ecg_record = await record_task
        return func.HttpResponse(body=ecg_record.to_json(), status_code=200)
    except Exception as e:
        return func.HttpResponse(body=str(e), status_code=400)


async def main(req: func.HttpRequest) -> func.HttpResponse:
    # import sys
    #
    # sys.path.append("path/to/pydevd-pycharm.egg")
    # import pydevd_pycharm
    #
    # pydevd_pycharm.settrace(
    #     "localhost", port=12345, stdoutToServer=True, stderrToServer=True
    # )

    logging.info("Python HTTP trigger function processed a request.")
    record_id = req.route_params.get("id")

    if not record_id:
        record_id = req.params.get("id")
    if not record_id:
        return func.HttpResponse(body="Record Id: {record_id} is invalid, please supply a valid numeric number",
                                 status_code=400)

    return await get_record(int(record_id))

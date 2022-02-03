import logging

import azure.functions as func
import pytest
from ecgai_training_data_physionet.models import EcgRecord

import ecgai_function_data_physionet


def module_logging_level():
    return logging.CRITICAL


def logger_name():
    return ""


# @pytest.mark.parametrize("record_id", invalid_record_id)
@pytest.mark.asyncio
async def test_get_ecg_record_with_valid_params():
    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='GET',
        body=None,
        url='/api/physionet/ptbxl/',
        params={'id': '56'})

    data = await ecgai_function_data_physionet.main(req)
    ecg = data.get_body()
    record = EcgRecord.from_json(ecg)
    assert type(record) is EcgRecord


@pytest.mark.asyncio
async def test_get_ecg_record_with_valid_route_params():
    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='GET',
        body=None,
        url='/api/physionet/ptbxl/',
        route_params={'id': '56'})

    data = await ecgai_function_data_physionet.main(req)
    ecg = data.get_body()
    record = EcgRecord.from_json(ecg)
    assert type(record) is EcgRecord


@pytest.mark.asyncio
async def test_get_ecg_record_with_invalid_route_params():
    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='GET',
        body=None,
        url='/api/physionet/ptbxl/')

    data = await ecgai_function_data_physionet.main(req)
    assert data.status_code == 400


@pytest.mark.asyncio
async def test_get_ecg_record_with_valid_route_params_invalid_id_outside_valid_range():
    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='GET',
        body=None,
        url='/api/physionet/ptbxl/',
        route_params={'id': '56000'})

    data = await ecgai_function_data_physionet.main(req)
    assert data.status_code == 400
    assert data.get_body() == b'The record was not found record_id 56000'
    print(data.get_body())

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def send_success_response(data, status_code=200):
    return JSONResponse(content={'error': None, 'data': jsonable_encoder(data), 'status': True}, status_code=status_code)


def send_failed_response(error, status_code=400):
    return JSONResponse(content={'error': error, 'data': None, 'status': False}, status_code=status_code)

"""All exception_handler logic are located here."""

import logging

from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from src.data_classes.responses import HTTPErrorResponse
from src.db.exceptions import (
    CreateInstanceError,
    HasBalanceError,
    RecordNotFoundError,
    UpdateInstanceError,
)


async def response_exception(exception: Exception) -> JSONResponse:
    """Maps `exception` to a :class:`JSONResponse` and returns it.

    :param exception: The caught exception.
    :type exception: :class:`Exception`
    :return: The exception as a json response.
    :rtype: :class:`JSONResponse`
    """

    if isinstance(exception, ConnectionRefusedError):
        _, arg_2 = exception.args

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(
                HTTPErrorResponse(
                    message="No database connection.",  # type: ignore
                    details={"message": arg_2},  # type: ignore
                )
            ),
        )

    if issubclass(exception.__class__, RecordNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder(
                HTTPErrorResponse(
                    message=exception.message,  # type: ignore
                    details=exception.details,  # type: ignore
                )
            ),
        )

    if issubclass(exception.__class__, CreateInstanceError):
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=jsonable_encoder(
                HTTPErrorResponse(
                    message=exception.message,  # type: ignore
                    details=exception.details,  # type: ignore
                )
            ),
        )

    if issubclass(exception.__class__, UpdateInstanceError):
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=jsonable_encoder(
                HTTPErrorResponse(
                    message=exception.message,  # type: ignore
                    details=exception.details,  # type: ignore
                )
            ),
        )

    if issubclass(exception.__class__, HasBalanceError):
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=jsonable_encoder(
                HTTPErrorResponse(
                    message=exception.message,  # type: ignore
                    details=exception.details,  # type: ignore
                )
            ),
        )

    logging.exception(exception)

    # fastapi will catch any unhandled exception and will
    # map it to a 500 Internal Server Error response
    raise exception

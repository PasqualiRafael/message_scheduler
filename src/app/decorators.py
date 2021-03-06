from functools import wraps
from http import HTTPStatus

from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from .db import session
from .logs import get_logger

logger = get_logger(__name__)


def error_handler(func):
    @wraps(func)
    def _error_handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as exc:
            logger.info("ValidationError: %s", exc)
            json_response = exc.messages

            return jsonify(json_response), HTTPStatus.BAD_REQUEST.value

        except IntegrityError as exc:
            logger.info("IntegrityError: %s", exc)
            message = exc.args[0].strip()

            if "duplicate key value violates unique constraint" in message:
                message = message.split(
                    'duplicate key value violates unique constraint "'
                )[1]
                message = message.split("_")
                table, field = message[0], message[1]
                message = f"There is already a {table} registered with this {field}"

            json_response = {"message": message}
            session.rollback()

            return jsonify(json_response), HTTPStatus.BAD_REQUEST.value

        except Exception as exc:
            logger.info("Internal server error: %s", exc)
            json_response = {"message": "Internal server error"}

            return jsonify(json_response), HTTPStatus.INTERNAL_SERVER_ERROR.value

    return _error_handler

from http import HTTPStatus

from flask import jsonify

from .db import session
from .logs import get_logger

logger = get_logger(__name__)


def generic_delete_method(instance_id, model, request):
    logger.info("request: %s", request)
    logger.info("instance_id: %s", instance_id)
    instance_db = session.query(model).get(instance_id)
    if not instance_db:
        response = {"message": f"{model.__tablename__.capitalize()} not found"}
        return jsonify(response), HTTPStatus.NOT_FOUND.value

    session.delete(instance_db)
    session.commit()
    logger.info("user.deleted")

    return jsonify({}), HTTPStatus.NO_CONTENT.value

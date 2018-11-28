from flask import Blueprint
from app.api.v1 import user, client, token, coupon, quality, task, image
# from test.test_view import api


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)

    user.api.register(bp_v1)
    user.users.register(bp_v1)
    client.api.register(bp_v1)
    token.api.register(bp_v1)
    coupon.api.register(bp_v1)
    quality.api.register(bp_v1)
    task.api.register(bp_v1)
    image.api.register(bp_v1)
    # api.register(bp_v1)
    return bp_v1
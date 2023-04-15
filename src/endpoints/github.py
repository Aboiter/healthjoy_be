from flask import request
from src.log import log

from src.exceptions import ValidationError
from src.blueprint import github_api

from src.ghub import GHub


@github_api.route("/fork", methods=["POST"])
@log()
def fork():
    g = GHub()

    data: dict = request.json

    # TODO: A better way to validate data can be either `JsonSchema` or `Cerberus`.
    if not data.get("access_token"):
        raise ValidationError(description="Please add access token.")

    if not data.get("repository_name"):
        raise ValidationError(description="Please add repository name.")

    return g.fork(**data)


@github_api.route("/list", methods=["GET"])
@log()
def list_repos():
    return GHub().list_repositories()

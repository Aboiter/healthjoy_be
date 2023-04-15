from flask import Blueprint

github_api = Blueprint("github_api", __name__, url_prefix="/api/v1")

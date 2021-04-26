"""
    FILE: api
    ---------
    This program implements the Brightwheel Email Service API.
"""

import json

import config
from utils import validate_email_fields

from bs4 import BeautifulSoup
from sanic import Sanic
from sanic import response
import requests


# CONSTANTS
# ---------
HTTP_OK, HTTP_CLIENT_ERROR = 200, 404

# GLOBAL VARIABLES:
# -----------------
# `app` - instance of the Sanic application in execution.
#
app = Sanic(__name__)

# FUNCTION: index
# ---------------
# Parameters:
#     `request` (object) - includes properties of an HTTP request such as
#     URL, headers, etc.
#
# Returns:
#     `response` (object) - an HTTP response.
#
# This function acts as a simple landing page when starting the application.
#
@app.route("/", methods=['GET'])
def index(request):
    return response.json({"Welcome to the Brightwheel Email Server API!": \
        "By Daniel George and your friends in Brightwheel Engineering"}, status=200)

# FUNCTION: email
# ---------------
# Parameters:
#     `request` (object) - includes properties of an HTTP request such as
#     URL, headers, etc.
#
# Returns:
#     `response` (object) - an HTTP response.
#
# This function accepts POST requests and redirects those requests to one of
# two 3rd-party services.
#
@app.route("/email", methods=['POST'])
async def email(request):
    data, headers = request.json, dict(request.headers)

    # ensure that a request contains all necessary fields
    if not validate_email_fields(data.keys()):
        return response.empty(status=HTTP_CLIENT_ERROR)

    # convert body from HTML to plain text
    data["body"] = BeautifulSoup(data["body"], features="html.parser").get_text('\n')

    # convert headers to acceptable header format
    headers = {'Content-Type': headers.get("content-type"), 'X-Api-Key': headers.get("x-api-key")}

    if config.EMAIL_SERVICE_PROVIDER == "SPENDGRID":
        # convert data to acceptable payload format for Spendgrid
        data = {
            'sender': '{} <{}>'.format(data.get("from_name"), data.get("from")),
            'recipient': '{} <{}>'.format(data.get("to_name"), data.get("to")),
            'subject': data.get("subject"),
            'body': data.get("body")}

        res = requests.post(
            url=config.SPENDGRID_URL,
            data=json.dumps(data),
            headers=headers)

        if res.ok:
            return response.json({"message": res.text}, status=res.status_code)
        else:
            return response.empty(status=res.status_code)

    elif config.EMAIL_SERVICE_PROVIDER == "SNAILGUN":
        # convert data to acceptable payload format for Snailgun
        data = {
            "from_email": data.get("from"),
            "from_name": data.get("from_name"),
            "to_email": data.get("to"),
            "to_name": data.get("to_name"),
            'subject': data.get("subject"),
            'body': data.get("body")}

        res = requests.post(
            url=config.SNAILGUN_URL,
            data=json.dumps(data),
            headers=headers)

        if res.ok:
            return response.json({"message": res.text}, status=res.status_code)
        else:
            return response.empty(status=res.status_code)

if __name__ == "__main__":
    app.run()

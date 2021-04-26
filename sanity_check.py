"""
    FILE: sanity_check
    ------------------
    This program implements unit tests for the
    Brightwheel Email Server API.
"""

import json
import unittest

import requests

from api import app
import config


class BasicTestSuite(unittest.TestCase):
    body = {"to": "susan@abcpreschool.org",
                "to_name": "Miss Susan",
                "from": "noreply@mybrightwheel.com",
                "from_name": "brightwheel",
                "subject": "Your Weekly Report",
                "body": "<h1>Weekly Report</h1><p>You saved 10 hours this week!</p>"}

    # THIS IS VERY BAD PRACTICE!!!  Including here in this test file for
    # time.  Fix is to use argparse with unittest so that this key can
    # be entered on the command line or use storage like AWS KMS or the like.
    spendgrid_api_key = "api_key_S0Uem3G0qIDeLfIptWhcVlPv"
    snailgun_api_key = "api_key_Dn2Dn3SdUEEriy4mPjK6VZNS"

    # Test that the landing page returns an HTTP OK code when invoked.
    def test_index_returns_200(self):
        request, response = app.test_client.get("/")
        assert response.status == 200

    # Test HTTP Client Error if passed too many fields.
    def test_too_many_email_fields(self):
        data = self.body
        data["unecessary_field"] = "123"
        request, response = app.test_client.post('/email', data=json.dumps(data))
        assert response.status == 404

    # Test HTTP Client Error if passed no fields.
    def test_no_email_fields(self):
        data = {}
        request, response = app.test_client.post('/email', data=json.dumps(data))
        assert response.status == 404

    # Test success when Spendgrid endpoint invoked.
    def test_success_sendgrid(self):
        if config.EMAIL_SERVICE_PROVIDER != "SENDGRID":
            pass
        else:
            headers = {'content-type': "application/json", 'x-api-key': self.spendgrid_api_key}
            data = self.body
            request, response = app.test_client.post('/email', data=json.dumps(data), headers=headers)
            assert response.status == 201

    # Test success when Snailgun endpoint invoked, meaning that the email has
    # either been sent, or is queued up to be sent.
    def test_success_snailgun(self):
        if config.EMAIL_SERVICE_PROVIDER != "SNAILGUN":
            pass
        else:
            headers = {'content-type': "application/json", 'x-api-key': self.snailgun_api_key}
            data = self.body
            request, response = app.test_client.post('/email', data=json.dumps(data), headers=headers)

            id = json.loads(response.json["message"]).get("id")
            url = ''.join([config.SNAILGUN_STATUS_URL, id])
            res = requests.get(url=url, headers=headers)
            res = json.loads(res.text)
            assert res.get("status") in ["queued", "sent"]

if __name__ == '__main__':
    unittest.main()

"""
    FILE: bwemail
    -------------
    This program implements an argument parser which parses the
    body of an email JSON object as well as an API Key for a
    given 3rd-party service.  Then, it calls the Brightwheel
    Email Server API.
"""
import argparse
import config

import requests


# FUNCTION: main
# --------------
# This function parses command line arguments, including the body of information
# pertaining to an email and an API Key corresponding with the 3rd-party service
# the application is directed to.
#
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--body", help="JSON body of email attributes", required=True)
    parser.add_argument("-k", "--key", help="an API Key corresponding with the 3rd-party email service", required=True)
    args = parser.parse_args()

    headers = {"Content-Type": "application/json",
               "X-Api-Key": args.key}

    return requests.post(
        url=config.BRIGHTWHEEL_EMAIL_SERVICE,
        data=args.body,
        headers=headers)

if __name__ == '__main__':
    main()

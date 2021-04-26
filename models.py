"""
    FILE: models
    ------------

    This program implements the data schema for the Email Server API.
    It consists of one model, an `Email`.
"""


# CLASS: Email
# ------------
# The `Email` class consists of the following class-level attributes:
#     (1) `to_email` (str) - the email address to send to.
#     (2) `to_name` (str) - the name to accompany the email.
#     (3) `from_email` (str) - the email address in the "from" and "reply" fields.
#     (4) `from_name` (str) - the name to accompany the from/reply emails.
#     (5) `subject` (str) - the subject line of the email.
#     (6) `body` (str) - the HTML body of the email.
#
class Email:
    def __init__(self):
        self.to_email = str()
        self.to_name = str()
        self.from_email = str()
        self.from_name = str()
        self.subject = str()
        self.body = str()

"""
    FILE: utils
    -----------
    This program implements utility methods pertaining to
    the Brightwheel Email Server API.
"""

from models import Email


# FUNCTION: validate_email_fields
# -------------------------------
# This function validates fields provided to the Brightwheel
# Email Server API by ensuring that the provided fields match
# those defined by the data schema.
#
def validate_email_fields(provided_fields):
    # A list of class attributes from the Email model.
    required_fields = list(vars(Email()).keys())
    provided_fields = list(provided_fields)

    # Two email fields, namely: `to` and `from`, are equivalently
    # `to_email` and `from_email` in our data model.
    for i in range(len(provided_fields)):
        if provided_fields[i] == "to":
            provided_fields[i] = "to_email"
        if provided_fields[i] == "from":
            provided_fields[i] = "from_email"

    if provided_fields != required_fields:
        return False

    return True

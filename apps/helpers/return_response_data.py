"""Helper functions to return response data for success and error request"""

def okay_response(response):
    """
    returns success response
    """
    data = {
        "status": "success",
        "data" : response
    }
    return data


def error_response(error, message):
    """
    returns error response
    """
    data = {
        "status": "error",
        "error": error,
        "message": message
    }
    return data

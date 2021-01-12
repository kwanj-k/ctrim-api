"""Helper function to save serializer"""


def save_serializer(serializer):
    """returns a particular response for when serializer passed is valid or not"""
    serializer.save()
    data = {
        "status": "success",
        "data": serializer.data
    }
    return data

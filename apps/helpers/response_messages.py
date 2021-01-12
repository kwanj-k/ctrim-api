"""http and socket response messages in one place for re usability"""
auth_messages = {
    "token_required": {
        "status": "error",
        "error": "token_not_found",
        "message": "Ensure request headers contain a token",
    },
    "expired_token": {
        'status': 'error',
        'error': 'token_expired',
        'message': 'Get a new token'
    },
    "invalid_token": {
        'status': 'error',
        'error': 'Invalid token',
        'message': 'Ensure you are using a Goauth token'
    },
    "not_found": {
        'status': 'error',
        'error': 'does_not_exist',
        'message': 'User Does not exist'
    },
    "requires_role": {
        'status': 'error',
        'error': 'unauthorized user',
        'message': 'You do not have the role priviledges to perform this action'
    }
}

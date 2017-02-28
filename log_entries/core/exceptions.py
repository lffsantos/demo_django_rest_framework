from rest_framework.exceptions import APIException


class UnauthorizedAccess(APIException):
    status_code = 401
    default_detail = 'User Unauthorized.'
    default_code = 'unauthorized_access'
import sys
from django.db import OperationalError
from django.http import JsonResponse
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if hasattr(exc, "error_code"):
            response.data["error_code"] = exc.error_code
            response.data["error_message"] = exc.default_detail

    return response


class LibidoApiException(APIException):
    status_code = 200
    error_code = 99999
    default_detail = "Internal Server Error"

    def get_error_message(self):
        return self.default_detail

    def get_response(self):
        return Response(
            {
                "success": False,
                "error_code": str(self.error_code),
                "error_message": self.get_error_message(),
            },
            status=self.status_code,
        )

    def get_json_response(self):
        return JsonResponse(
            {
                "success": False,
                "error_code": str(self.error_code),
                "error_message": self.get_error_message(),
            },
            status=self.status_code,
        )


class InvalidRoomPasswordError(LibidoApiException):
    error_code = 13
    status_code = 400
    default_detail = "InvalidRoomPasswordError"


class InvalidEmailAddressError(LibidoApiException):
    error_code = 14
    status_code = 400
    default_detail = "InvalidEmailAddressError"


class EmailAuthConfirmError(LibidoApiException):
    error_code = 15
    status_code = 400
    default_detail = "EmailAuthConfirmError"


class RoomNotFoundError(LibidoApiException):
    error_code = 700
    status_code = 200
    default_detail = "RoomNotFound Error"
    default_code = 700


class UserIdNotFoundError(LibidoApiException):
    error_code = 1110
    status_code = 200
    default_detail = "UserIdNotFound Error"
    default_code = 1110


class InvalidUserPasswordError(LibidoApiException):
    error_code = 1111
    status_code = 200
    default_detail = "InvalidUserPassword Error"
    default_code = 1111


class InvalidOauth2ClientIdOrSecretError(LibidoApiException):
    error_code = 1112
    status_code = 200
    default_detail = "InvalidOauth2ClientIdOrSecret Error"
    default_code = 1112


class UnSupportedGrantTypeError(LibidoApiException):
    error_code = 1113
    status_code = 200
    default_detail = "UnSupportedGrantType Error"
    default_code = 1113


class InvalidBitCoinAddress(LibidoApiException):
    error_code = 10000
    status_code = 200
    default_detail = "Invalid Bitcoin address"
    default_code = 10000


class InvalidBitCoinAddressOrWebAddress(LibidoApiException):
    error_code = 10001
    status_code = 200
    default_detail = "Invalid Bitcoin address or Invalid Web URL"
    default_code = 10001


class IncorrectPinNoError(LibidoApiException):
    error_code = 10002
    status_code = 200
    default_detail = "Incorrect Pinno Error"
    default_code = 10002


class WalletAlreadyExistsError(LibidoApiException):
    error_code = 10003
    status_code = 200
    default_detail = "Cannot Generate Wallet - already exists"
    default_code = 10003


class InvalidSmsAuthKeyAndMobileNumberError(LibidoApiException):
    error_code = 10004
    status_code = 200
    default_detail = "Invalid SmsauthKey and MobileNumber Error"
    default_code = 10004


# insufficient balance
class InsufficientFundsError(LibidoApiException):
    error_code = 10005
    status_code = 200
    default_detail = "Insufficient Funds"
    default_code = 10005


# tmp token error
class CreateTmpTokenError(LibidoApiException):
    error_code = 10006
    status_code = 200
    default_detail = "CreateTmpTokenError"
    default_code = 10006


class SmsAuthValidationError(LibidoApiException):
    error_code = 10007
    status_code = 200
    default_detail = "SmsAuthValidationError"
    default_code = 10007


class SendCoinMinAmountError(LibidoApiException):
    error_code = 13000
    status_code = 200
    default_detail = "SendCoinMinAmountError"
    default_code = 13000


class SendCoinMaxAmountError(LibidoApiException):
    error_code = 13001
    status_code = 200
    default_detail = "SendCoinMaxAmountError"
    default_code = 13001


class KrwDepositMinAmountError(LibidoApiException):
    error_code = 13002
    status_code = 200
    default_detail = "KrwDepositMinAmountError"
    default_code = 13002


class KrwDepositPreviousRequestExists(LibidoApiException):
    error_code = 13003
    status_code = 200
    default_detail = "KrwDepositPreviousRequestExists"
    default_code = 13003


class CreateUserLinkError(LibidoApiException):
    error_code = 50000
    status_code = 200
    default_detail = "CreateUserLinkError"
    default_code = 50000


class CreateBookmarkUserError(LibidoApiException):
    error_code = 50001
    status_code = 200
    default_detail = "CreateBookmarkUserError"
    default_code = 50001


# class UserDoesNotExists(LibidoApiException):
#     error_code = 70000
#     status_code = 200
#     default_detail = "CreateUserLinkError"
#     default_code = 70000
#


class LibidoUnknownAuthError(LibidoApiException):
    error_code = 10000
    status_code = 200
    default_detail = "Unknwon auth error"
    default_code = 10000


class LibidoFirebaseAuthDecodeError(LibidoApiException):
    error_code = 10001
    status_code = 200
    default_detail = "LibidoFirebaseAuthDecodeError"
    default_code = 10001


class LibidoFirebaseInvalidIDTokenProvidError(LibidoApiException):
    error_code = 10002
    status_code = 200
    default_detail = "ValueError: Illegal ID token provided"
    default_code = 10002


class LibidoFormDataError(LibidoApiException):
    error_code = 99998
    status_code = 200
    default_detail = "Form data error"
    default_code = 99998


class LibidoUnknownError(LibidoApiException):
    error_code = 99999
    status_code = 200
    default_detail = "Unknown sysyem error"
    default_code = 99999

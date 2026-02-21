from Utils.CustomException import APIException


class AppErrors:
    @staticmethod
    def bad_request(msg: str = "Bad Request"):
        return APIException(400, msg, "INVALID_INPUT")

    @staticmethod
    def unauthorized(msg: str = "Unauthorized"):
        return APIException(401, msg, "AUTH_REQUIRED")

    @staticmethod
    def not_found(msg: str = "Resource not found"):
        return APIException(404, msg, "NOT_FOUND")

    @staticmethod
    def rate_limit(msg: str = "Too many requests"):
        return APIException(429, msg, "SLOW_DOWN")

    @staticmethod
    def internal(msg: str = "Internal server error"):
        return APIException(500, msg, "SERVER_FAULT")

    @staticmethod
    def custom(code: int, msg: str, label: str):
        return APIException(code, msg, label)
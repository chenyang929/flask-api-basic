from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = 'sorry, we make a mistake'
    error_code = 999

    def __init__(self, msg=None, code=None, error_code=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]


# 400 请求参数错误
# 401 未授权
# 403 禁止访问
# 404 没有找到资源
# 500 服务器产生未知错误
# 200 请求成功，201 创建或更新成，204 删除成功


class Success(APIException):
    code = 201
    msg = 'ok'
    error_code = 0


class DeleteSuccess(Success):
    code = 202   # 204的话不会返回任何值
    error_code = 1


class ServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake'
    error_code = 999


class ClientTypeError(APIException):
    code = 400
    msg = 'client is invalid'
    error_code = 1006


class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class NotFound(APIException):
    code = 404
    msg = 'the resource are not_found'
    error_code = 1001


class AuthFailed(APIException):
    code = 401  # 401授权失败
    msg = 'authorization failed'
    error_code = 1005


class Forbidden(APIException):
    code = 403   # 403禁止访问
    error_code = 1004
    msg = 'forbidden, not in scope'


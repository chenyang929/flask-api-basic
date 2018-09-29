class Scope:
    allow_api = []
    allow_module = []
    forbidden_api = []

    def __add__(self, other):
        self.allow_api = list(set(self.allow_api + other.allow_api))
        self.allow_module = list(set(self.allow_module + other.allow_module))
        self.forbidden_api = list(set(self.forbidden_api + other.forbidden_api))


class UserScope(Scope):
    allow_api = ['v1.user+get_user']
    #forbidden_api = ['v1.user+super_get_user']

    def __init__(self):
        pass
        #self + AdminScope()


class AdminScope(Scope):
    #allow_api = ['v1.user+super_get_user']
    allow_module = ['v1.user']

    def __init__(self):
        self + UserScope()


def is_in_scope(scope, endpoint):
    gl = globals()   # 包含该py文件里全部对象，字典形式
    scope = gl[scope]()  # 动态生成python对象，这里是类
    splits = endpoint.split('+')
    red_name = splits[0]
    if endpoint in scope.forbidden_api:
        return False
    elif endpoint in scope.allow_api:
        return True
    elif red_name in scope.allow_module:
        return True
    else:
        return False

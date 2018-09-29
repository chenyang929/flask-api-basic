from flask import current_app, jsonify
from app.libs.error import AuthFailed
from app.libs.redprint import Redprint
from app.validators.form import ClientForm, TokenForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from app.models.mongo import mongo
from werkzeug.security import check_password_hash


api = Redprint('token')


@api.route('', methods=['POST'])
def get_token():
    form = ClientForm().validate_for_api()
    user_info = _verify_user_info(form)
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(str(user_info['_id']),
                                user_info['scope'],
                                expiration)
    t = {'token': token.decode('ascii')}
    return jsonify(t), 201


def _verify_user_info(form):
    user_info = mongo.db.user.find_one_or_404({'email': form.account.data})
    if not check_password_hash(user_info['password'], form.secret.data):
        raise AuthFailed()
    user_info['scope'] = 'AdminScope' if user_info['auth'] == 2 else 'UserScope'
    return user_info


@api.route('/secret', methods=['POST'])
def get_token_info():
    """验证令牌信息"""
    form = TokenForm().validate_for_api()
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(form.token.data, return_header=True)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)
    r = {
        'scope': data[0]['scope'],
        'create_at': data[1]['iat'],  # 同下itsdangerous生成的
        'expire_in': data[1]['exp'],
        'uid': data[0]['uid']
    }
    # 实际可以不返回任何信息或有选择的返回
    return jsonify(r)


def generate_auth_token(uid, scope=None, expiration=7200):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({
        'uid': uid,
        'scope': scope,
    })

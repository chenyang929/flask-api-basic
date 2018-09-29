from app.libs.error import Success
from app.libs.redprint import Redprint
from app.validators.form import ClientForm, UserEmailForm
from app.libs.enums import ClientTypeEnum
from app.models.mongo import mongo
from werkzeug.security import generate_password_hash


api = Redprint('client')


@api.route('/register', methods=['POST'])
def create_client():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email
    }
    promise[form.type.data]()
    return Success()


def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    user_info = {'email': form.account.data,
                 'nickname': form.nickname.data,
                 'password': generate_password_hash(form.secret.data),
                 'auth': 1}
    mongo.db.user.insert_one(user_info)

from flask import request
from wtforms import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError
from app.libs.error import ParameterException
from app.libs.enums import ClientTypeEnum
from app.models.mongo import mongo


class BaseForm(Form):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise ParameterException(msg=self.errors)
        return self


class ClientForm(BaseForm):
    account = StringField(validators=[DataRequired(message='不允许为空'), length(min=5, max=32)])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:   # 异常不会抛出，会记录在form.errors中
            raise e
        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[Email(message='无效的邮箱')])
    secret = StringField(validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')])
    nickname = StringField(validators=[DataRequired(), length(min=2, max=22)])

    def validate_account(self, value):
        if mongo.db.user.find_one({'email': value.data}):
            raise ValidationError(message='邮箱已被注册')

    def validate_nickname(self, value):
        if mongo.db.user.find_one({'nickname': value.data}):
            raise ValidationError(message='昵称已被注册')


class TokenForm(BaseForm):
    token = StringField(validators=[DataRequired(message='不允许为空')])


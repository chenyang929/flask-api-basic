from flask import jsonify, g
from app.libs.error import DeleteSuccess
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.mongo import mongo
from bson.objectid import ObjectId

api = Redprint('user')


@api.route('/<string:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    user = mongo.db.user.find_one_or_404({'_id': ObjectId(uid)})
    return jsonify(user)


@api.route('', methods=['GET'])
@auth.login_required
def get_user():
    uid = g.user.uid
    user = mongo.db.user.find_one_or_404({'_id': ObjectId(uid)}, {'email': 1, 'nickname': 1})
    return jsonify(user)


@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    uid = g.user.uid
    mongo.db.user.update({'_id': ObjectId(uid)}, {"$set": {"status": 0}})
    return DeleteSuccess()


@api.route('/test')
def hello():
    return jsonify({'hello': 'ok'})


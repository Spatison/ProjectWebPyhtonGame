from flask_restful import reqparse, abort, Resource
from flask import jsonify
from .users import User
from . import db_session

parser = reqparse.RequestParser()
parser.add_argument('nickname', required=True)
parser.add_argument('email', required=True)


def abort_if_news_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only='nickname')})

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        user = session.query(User).get(news_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only='nickname') for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        news = User(
            nickname=args['nickname'],
            email=args['email']
        )
        session.add(news)
        session.commit()
        return jsonify({'id': news.id})

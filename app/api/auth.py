from uuid import uuid4

from flask import request
from flask_restx import Resource
from app.api import auth_api
from secrets import token_urlsafe

from app.helpers.auth import email_exists, username_exists
from app.models.users import Users
import app.context as ctx
from app.helpers.api_response import UserApiResponse, BaseApiResponse


@auth_api.route('/login')
class Login(Resource):

    def post(self):
        form = request.get_json()
        res = UserApiResponse()

        try:
            user = Users.query.filter((Users.email == form["username"]) | (Users.username == form["username"])).first()
        except KeyError:
            res.add_error("Username cannot be empty")
            return res.make()

        if not user:
            res.add_error("Invalid credentials")
            return res.make(), 404

        try:
            if not user.check_password(form.get("password", "")):
                res.add_error("Invalid credentials")
                return res.make()
        except ValueError:
            res.add_error("Failed to check the password. Please contact an administrator.")
            return res.make(), 500

        # set cookie in db
        session = token_urlsafe(128)
        user.update_last_login()
        user.session = session
        ctx.db.session.commit()

        res.set_user(user, public=False)

        return res.make()


@auth_api.route('/register')
class Register(Resource):

    def post(self):
        form = request.get_json()
        res = UserApiResponse()
        required = ["username", "password"]

        for field in required:
            if field not in form:
                res.add_error(f"{field.title()} is missing")
                return res.make()

        for key, val in form.items():
            if not val:
                res.add_error(f"{key.title()} is missing")
                return res.make()

        if form.get("email"):
            if email_exists(form["email"], ctx):
                res.add_error("An account with this email already exists")
                return res.make()

        if username_exists(form["username"], ctx):
            res.add_error("An account with this username already exists")
            return res.make()

        if form["password"] == "":
            res.add_error("Password is missing")
            return res.make()

        session = token_urlsafe(128)

        new_user = Users(id=uuid4(), username=form["username"], email=form.get("email", None))
        new_user.set_password(form["password"])
        new_user.session = session

        ctx.db.session.add(new_user)
        ctx.db.session.commit()
        res.set_user(new_user, public=False)

        return res.make()


@auth_api.route('/check')
class Check(Resource):

    def post(self):
        data = request.get_json()
        session = data.get("session")
        res = UserApiResponse()

        if not session:
            return res.make()

        user = ctx.db.session.query(Users).filter_by(session=session).first()
        if not user:
            res.add_error("Invalid session")
            return res.make()

        res.set_user(user, public=False)

        return res.make()


@auth_api.route('/logout')
class Logout(Resource):

    def post(self):
        user_data = request.get_json()
        res = BaseApiResponse()

        try:
            user = ctx.db.session.query(Users).filter_by(email=user_data["email"]).first()
        except KeyError:
            res.add_error("Email cannot be empty")
            return res.make()

        if not user:
            res.add_error("Failed to get user")
            return res.make()

        user.session = ""
        ctx.db.session.commit()

        return res.make()


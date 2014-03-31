# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from flask import current_app
from wtforms import TextField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp
from wtforms.validators import Optional, URL

from app.account.models import Account


class SignupForm(Form):
    phone = TextField(
        u'登录手机号码', [
            DataRequired(), Regexp(r'^(13\d|15\d|18\d|14[57])\d{8}$')
            ]
    )
    password = PasswordField(u'密码', [DataRequired()])
    confirm = PasswordField(u'确认密码', [
        DataRequired(),
        EqualTo('password', message = 'Passwords must match')
        ])
    nickname = TextField(u'昵称', [DataRequired()])

    def validate_phone(self, field):
        if Account.query.filter_by(phone=field).count():
            raise ValueError(u'该手机号码已注册.')

    def save(self, role=None):
        user = Account(**self.data)
        if role:
            user.role = role
        user.save()
        return user

class SigninForm(Form):
    phone = TextField(
        u'登录手机号码', [
            DataRequired(), Regexp(r'^(13\d|15\d|18\d|14[57])\d{8}$')
            ]
    )
    password = PasswordField(u'密码', [DataRequired()])
    permanent = BooleanField(u'一个月内自动登录')

    def validate_password(self, field):
        phone = self.phone.data
        user = Account.query.filter_by(phone=phone).first()

        if not user:
            raise ValueError(u'用户或密码错误')
        if user.check_password(field.data):
            self.user = user
            return user
        raise ValueError(u'用户或密码错误')


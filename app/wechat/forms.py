# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, EqualTo

class LoginForm(Form):
    phone = TextField(u'手机号码', [Required()])
    password = PasswordField(u'密码', [Required()])

class RegisterForm(Form):
    phone = TextField(u'登录手机号码', [Required()])
    password = PasswordField(u'密码', [Required()])
    confirm = PasswordField(u'确认密码', [
        Required(),
        EqualTo('password', message = 'Passwords must match')
        ])
    nickname = TextField(u'昵称', [Required()])

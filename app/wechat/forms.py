# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, SelectField
from wtforms.validators import Required

class AddWxuserForm(Form):
    wxname = TextField(u'公众号名称', [Required()])
    wxid = TextField(u'公众号原始id', [Required()])
    weixin = TextField(u'微信号', [Required()])
    headerpic = TextField(u'头像地址')
    typeid = SelectField(u'账号类型', coerce=int, choices=[(0, u'订阅号'), (1, u'服务号')])

    appid = TextField('AppID')
    appsecret = TextField('AppSecret')



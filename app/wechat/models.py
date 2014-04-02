# -*- coding: utf-8 -*-

from app import db
from app.account.models import Account

from flask import g
import hashlib
import datetime

class Wxuser(db.Model):

    __tablename__ = 'wechat_wxuser'
    id = db.Column(db.Integer, primary_key=True)
    wxname = db.Column(db.String(20))
    wxid = db.Column(db.String(20), unique=True)
    weixin = db.Column(db.String(20))
    headerpic = db.Column(db.String(255))
    token = db.Column(db.String(32))
    typeid = db.Column(db.Integer)

    appid = db.Column(db.String(32))
    appsecret = db.Column(db.String(32))

    created = db.Column(db.Date)
    deadtime = db.Column(db.Date)


    def __init__(self, **kwargs):

        self.created = datetime.date.today()
        self.deadtime = datetime.date.today() + datetime.timedelta(days=3)

        for k, v in kwargs.items():
            setattr(self, k, v)
        self.token = hashlib.md5(kwargs.get('wxid', '')+'zhufeng').hexdigest()

    def save(self):
        db.session.add(self)
        db.session.commit()

        aw = AccountAndWxuser(wxuser_id=self.id)
        aw.save()
        return self

    def getToken(self):
        return self.token


    def __repr__(self):
        return '<Wxuser %>' % self.wxname

class AccountAndWxuser(db.Model):

    __tablename__ = 'rel_account_wxuser'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, nullable=False, index=True)
    wxuser_id = db.Column(db.Integer, nullable=False, index=True)
    role = db.Column(db.String(10), default='staff')

    def __init__(self, **kwargs):
        self.account_id = g.user.id

        for k, v in kwargs.items():
            setattr(self, k, v)

    def save(self):
        db.session.add(self)
        db.session.commit()







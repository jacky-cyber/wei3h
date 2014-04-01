# -*- coding: utf-8 -*-

from app import db

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
        return self

    def getToken(self):
        return self.token


    def __repr__(self):
        return '<Wxuser %>' % self.wxname









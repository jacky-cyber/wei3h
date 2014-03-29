# -*- coding: utf-8 -*-

from app import db

class User(db.Model):

    __tablename__ = 'wechat_user'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(11), unique=True)
    password = db.Column(db.String(120))
    nickname = db.Column(db.String(20), unique=True)

    createtime = db.Column(db.BigInteger)
    lastlogintime = db.Column(db.BigInteger)
    lastloginip = db.Column(db.String(20))

    def __init__(self, phone=None, password=None, nickname=None, \
        createtime=None, lastlogintime=None, lastloginip=None):
        self.phone = phone
        self.password = password
        self.nickname = nickname

        self.createtime = createtime
        self.lastlogintime = lastlogintime
        self.lastloginip = lastloginip

    def __repr__(self):
        return '<User %>' % self.phone









# -*- coding: utf-8 -*-

from app import db

import hashlib
import time

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

    createtime = db.Column(db.BigInteger)
    deadtime = db.Column(db.BigInteger) # createtime + 86400


    def __init__(self, wxname=None, wxid=None, weixin=None, \
        headerpic=None, typeid=0, appid='', appsecret=''):
        self.wxname = wxname
        self.wxid = wxid
        self.weixin = weixin
        self.headerpic = headerpic
        self.token = hashlib.md5(wxid+'zhufeng').hexdigest()
        self.typeid = typeid

        self.appid = appid
        self.appsecret = appsecret

        t = int(time.time())
        self.createtime = t
        self.deadtime = t + 86400

    def getToken(self):
        return self.token


    def __repr__(self):
        return '<Wxuser %>' % self.wxname









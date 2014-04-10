# -*- coding: utf-8 -*-

from app import db

from flask import g
from werkzeug import security

class Shop(db.Model):

    __tablename__ = 'weshop_shop'
    id = db.Column(db.Integer, primary_key=True)
    wxuser_id = db.Column(db.Integer, nullable=False, index=True)
    title = db.Column(db.String(32))
    token = db.Column(db.String(20), nullable=False, index=True)


    def __init__(self, **kwargs):

        self.wxuser_id = g.wxuser.id
        self.token = security.gen_salt(length)

        for k, v in kwargs.items():
            setattr(self, k, v)

    def save(self):
        db.session.add(self)
        db.session.commit()

        return self

    def getToken(self):
        return self.token


    def __repr__(self):
        return '<weshop %>' % self.title





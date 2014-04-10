# -*- coding: utf-8 -*-

from app import db

import hashlib
from datetime import datetime
from werkzeug import security

class Account(db.Model):

    __tablename__ = 'account_user'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(11), unique=True, index=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    nickname = db.Column(db.String(20), unique=True)

    role = db.Column(db.String(10), default='user')

    created = db.Column(db.DateTime, default=datetime.now)
    token = db.Column(db.String(20))

    def __init__(self, **kwargs):
        self.token = self.create_token(16)

        if 'password' in kwargs:
            raw = kwargs.pop('password')
            self.password = self.create_password(raw)

        for k, v in kwargs.items():
            setattr(self, k, v)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __str__(self):
        return self.nickname or self.phone

    def __repr__(self):
        return '<User %s>' % self.phone

    @staticmethod
    def create_password(raw):
        print db.app.config['PASSWORD_SECRET']
        passwd = '%s%s' % (raw, db.app.config['PASSWORD_SECRET'])
        return security.generate_password_hash(passwd)

    @staticmethod
    def create_token(length=16):
        return security.gen_salt(length)

    @property
    def is_staff(self):
        if self.id == 1:
            return True
        return self.role == 'staff' or self.role == 'admin'

    @property
    def is_admin(self):
        return self.id == 1 or self.role == 'admin'

    def check_password(self, raw):
        passwd = '%s%s' % (raw, db.app.config['PASSWORD_SECRET'])
        return security.check_password_hash(self.password, passwd)

    def change_password(self, raw):
        self.password = self.create_password(raw)
        self.token = self.create_token()
        return self










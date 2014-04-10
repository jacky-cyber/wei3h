# -*- coding: utf-8 -*-

from app import db

from flask import g
import hashlib
from datetime import datetime

class Filepage(db.Model):

    __tablename__ = 'dashboard_filepage'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, nullable=False, index=True)
    ptype = db.Column(db.String(20), nullable=False, index=True)
    filename = db.Column(db.String(255))
    url = db.Column(db.String(255))
    created = db.Column(db.Date, default=datetime.now)

    def __init__(self, **kwargs):
        self.account_id = g.user.id

        for k, v in kwargs.items():
            setattr(self, k, v)

    def getUrl(self):
        return self.url

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Filepage %s>' % self.filename





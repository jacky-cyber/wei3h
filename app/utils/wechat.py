# -*- coding: utf-8 -*-

import time

from app import db
from app.wechat.models import Follower

def add_follower(wxid=None, openid=None, follow_time=int(time.time()), last_active_time=int(time.time())):
    follower = Follower(wxid=wxid, openid=openid, follow_time=follow_time, last_active_time=last_active_time)
    follower.save()

    return follower.id

def delete_follower(wxid=None, openid=None):
    follower = Follower.query.filter_by(wxid=wxid, openid=openid).first()

    db.session.delete(follower)
    db.session.commit()

def update_follower(wxid=None, openid=None, last_active_time=int(time.time())):
    follower = Follower.query.filter(wxid=wxid, openid=openid).update(dict(last_active_time=last_active_time))
    db.session.commit()

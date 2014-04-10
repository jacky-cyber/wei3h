# -*- coding: utf-8 -*-


import functools
from flask import g, request, session, current_app, flash, url_for, redirect, abort
from app.wechat.models import Wxuser

class require_role():
    roles = {
        'user': 0,
        'staff': 1,
        'admin': 2,
    }

    def __init__(self, role):
        self.role = role

    def __call__(self, method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            if not g.user:
                url = url_for('account.signin')
                if '?' not in url:
                    url += '?next=' + request.url
                return redirect(url)
            if self.role is None:
                return method(*args, **kwargs)
            if g.user.id == 1:
                return method(*args, **kwargs)
            if self.roles[g.user.role] < self.roles[self.role]:
                return abort(403)
            return method(*args, **kwargs)
        return wrapper

require_login = require_role(None)
require_user = require_role('user')
require_staff = require_role('staff')
require_admin = require_role('admin')


def get_current_wxuser():
    if 'wxid' in session:
        wxuser = Wxuser.query.get(int(session['wxid']))
        if not wxuser:
            return None
        return wxuser
    return None

def login_wxuser(wxuser):

    if 'wxid' in session:
        session.pop('wxid')

    if not wxuser:
        return None
    session['wxid'] = wxuser.id

    return wxuser






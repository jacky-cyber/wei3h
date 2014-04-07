# -*- coding: utf-8 -*-

import datetime

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from ..utils.user import get_current_user, require_login

from app.wechat.forms import AddWxuserForm

from app.wechat.models import Wxuser, AccountAndWxuser

mod = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@mod.before_request
def before_request():
    g.user = get_current_user()

@mod.route('/')
@mod.route('/index/')
@require_login
def index():
    form = AddWxuserForm(request.form)
    wxusers = Wxuser.query.from_statement('select * from wechat_wxuser where id in (select wxuser_id from rel_account_wxuser where account_id = %d)' % g.user.id)
    return render_template('dashboard/index.html', today=datetime.date.today(), form=form, wxusers=wxusers)

@mod.route('/wxuser/<id>/home')
def wxuser_dashboard(id):
    wxuser = Wxuser.query.get(id)
    return render_template('dashboard/dashboard.html', wxuser=wxuser)

@mod.route('/wxuser/<id>/function/subscribe')
def wxuser_function_subscribe(id):
    wxuser = Wxuser.query.get(id)
    return render_template('dashboard/function_subscribe.html', wxuser=wxuser)



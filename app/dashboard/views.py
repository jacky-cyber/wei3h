# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from ..utils.user import get_current_user, require_login

from app.wechat.forms import AddWxuserForm

mod = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@mod.before_request
def before_request():
    g.user = get_current_user()

@mod.route('/')
@mod.route('/index/')
@require_login
def index():
    form = AddWxuserForm(request.form)
    return render_template('dashboard/index.html', form=form)


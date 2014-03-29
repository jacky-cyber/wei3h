# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash
from app import db

from app.wechat.models import User
from app.wechat.forms import LoginForm, RegisterForm
from app.wechat.decorators import requires_login

import time

mod = Blueprint('wechat', __name__, url_prefix='/wechat')

@mod.route('/home/')
@requires_login
def home():
    return g.user.phone + '<a href="/wechat/logout/">logout</a>'

@mod.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = User.query.get(session['user'])

@mod.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user'] = user.id
            flash('Welcome %s' % user.nickname)
            return redirect(url_for('wechat.home'))
        flash('Wrong email or password', 'error-message')
    return render_template('wechat/login.html', form=form)

@mod.route('/logout/')
def logout():
    session.pop('user', None)
    return redirect(url_for('wechat.login'))

@mod.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    t = int(time.time())
    if form.validate_on_submit():
        user = User(phone=form.phone.data, \
            password=generate_password_hash(form.password.data), \
            nickname=form.nickname.data, createtime=t, \
            lastlogintime=t, lastloginip=request.remote_addr)

        db.session.add(user)
        db.session.commit()

        session['user'] = user.id

        flash('Thanks for registering')
        return redirect(url_for('wechat.home'))
    return render_template('wechat/register.html', form=form)









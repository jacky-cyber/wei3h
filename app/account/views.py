# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app.account.models import Account
from app.account.forms import SignupForm, SigninForm
from ..utils.user import get_current_user, login_user, logout_user, require_login, verify_auth_token

mod = Blueprint('account', __name__, url_prefix='/account')

@mod.before_request
def before_request():
    g.user = get_current_user()

@mod.route('/home/')
@require_login
def home():
    return g.user.phone + '<a href="/account/signout/">logout</a>'

@mod.route('/signup/', methods=['POST', 'GET'])
def signup():
    next_url = request.args.get('next', url_for('dashboard.index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user)
        flash('thank you')
        return redirect(next_url)
    return render_template('account/signup.html', form=form)

@mod.route('/signin/', methods=['GET', 'POST'])
def signin():
    next_url = request.args.get('next', url_for('dashboard.index'))
    if g.user:
        return redirect(next_url)
    form = SigninForm()

    if form.validate_on_submit():
        login_user(form.user, form.permanent.data)
        return redirect(next_url)
    return render_template('account/signin.html', form=form)

@mod.route('/signout/')
def signout():
    next_url = request.args.get('next', url_for('.signin'))
    logout_user()
    return redirect(next_url)




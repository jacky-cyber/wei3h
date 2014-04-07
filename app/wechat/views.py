# -*- coding: utf-8 -*-

from flask import Blueprint, request, make_response, render_template, flash, g, session, redirect, url_for
from app import db

from app.wechat.models import Wxuser, Follower
from app.wechat.forms import AddWxuserForm


from ..utils.user import get_current_user
from ..utils.wechat import add_follower, delete_follower, update_follower
from ..wpi.api import *


mod = Blueprint('wechat', __name__, url_prefix='/wechat')

@mod.before_request
def before_request():
    g.user = get_current_user()

@mod.route('/home/<token>')
def home(token):
    return token

@mod.route('/addwechat/', methods=['GET', 'POST'])
def add_wechat():
    form = AddWxuserForm(request.form)


    if form.validate_on_submit():

        wxuser = form.save()

        flash('Thanks for registering ' + wxuser.getToken())
        return redirect(url_for('wechat.home', token=wxuser.getToken()))
    return render_template('wechat/add_wechat.html', form=form)

@mod.route('/api/<token>', methods=['GET', 'POST'])
def wechat_api(token):

    if request.method == 'GET':
        query = request.args

        return checkSignature(query, token)

    if request.method == 'POST':
        message = getMessage(request.data)
        print message

        ToUserName = message['ToUserName']
        FromUserName = message['FromUserName']
        CreateTime = message['CreateTime']
        MsgType = message['MsgType']

        if Follower.query.filter_by(wxid=ToUserName, openid=FromUserName).count() == 0:
            add_follower(ToUserName, FromUserName, 0, CreateTime)
        else:
            update_follower(ToUserName, FromUserName, CreateTime)


        if MsgType == 'event':
            if message['Event'] == 'subscribe':
                pass
            if message['Event'] == 'unsubscribe':
                delete_follower(ToUserName, FromUserName)


        r = reply('text', '朱峰', ToUserName, FromUserName)
        response = make_response(r)
        response.content_type = 'application/xml'
        return response






# -*- coding: utf-8 -*-

from flask import Blueprint, request, make_response, render_template, flash, g, session, redirect, url_for
from app import db

from app.wechat.models import Wxuser, Follower
from app.wechat.forms import AddWxuserForm


from ..utils.user import get_current_user
from ..utils.wechat import add_follower, delete_follower, update_follower
from ..wpi.api import *


mod = Blueprint('wechat', __name__, url_prefix='/wechat')

import pymongo
from bson.objectid import ObjectId
conn = pymongo.Connection('localhost', 5430)
db = conn.test

@mod.before_request
def before_request():
    g.user = get_current_user()

# @mod.route('/home/<token>')
# def home(token):
#     return token

@mod.route('/addwechat/', methods=['GET', 'POST'])
def add_wechat():
    form = AddWxuserForm(request.form)


    if form.validate_on_submit():

        wxuser = form.save()

        return redirect(url_for('dashboard.index'))
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

        s = ''

        if Follower.query.filter_by(wxid=ToUserName, openid=FromUserName).count() == 0:
            add_follower(ToUserName, FromUserName, CreateTime, CreateTime)
        else:
            update_follower(ToUserName, FromUserName, CreateTime)


        if MsgType == 'event':
            if message['Event'] == 'subscribe':
                pass
            if message['Event'] == 'unsubscribe':
                delete_follower(ToUserName, FromUserName)
        elif MsgType == 'text':
            get_content = message['Content']
            re = db.reply.find_one({'wxid': ToUserName, 'msgtype': 'text', 'keyword': get_content}, {'_id': 0})

            if re is None:
                re = db.reply.find_one({'wxid': ToUserName, 'msgtype': 'text', 'keyword': 'pdlerfzahufletn'}, {'_id': 0})
            s = re.get('content', '')

        r = reply('text', s, ToUserName, FromUserName)
        response = make_response(r)
        response.content_type = 'application/xml'
        return response






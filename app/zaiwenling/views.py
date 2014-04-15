# -*- coding: utf-8 -*-

from flask import Blueprint, request, make_response, render_template, flash, g, session, redirect, url_for

from app import db as mdb
from app.zaiwenling.forms import MusicForm
from app.zaiwenling.models import Music

from app.wechat.models import Follower

from ..utils.wechat import add_follower, delete_follower, update_follower
from ..wpi.api import *

mod = Blueprint('zaiwenling', __name__, url_prefix='/zaiwenling')


import pymongo
from bson.objectid import ObjectId
conn = pymongo.Connection('localhost', 5430)
db = conn.test

@mod.route('/index/')
@mod.route('/')
def index():
    return render_template('zaiwenling/index.html')

@mod.route('/addmusic/', methods=['GET', 'POST'])
def add_music():
    form = MusicForm(request.form)
    if form.validate_on_submit():

        music = Music(music_title=form.music_title.data, music_artist=form.music_artist.data, music_pic=form.music_pic.data, music_audio=form.music_audio.data)

        mdb.session.add(music)
        mdb.session.commit()

        return redirect(url_for('zaiwenling.list_music'))
    return render_template('zaiwenling/add_music.html', form=form)

@mod.route('/music/<id>/')
def get_music(id):
    music = Music.query.filter_by(id=id).first()
    return render_template('zaiwenling/music.html', music=music)

@mod.route('/musics/')
def list_music():
    musics = Music.query.all()
    return render_template('zaiwenling/musics.html', musics=musics)

@mod.route('/waimai/<id>/')
def get_waimai(id):
    waimai = db.waimai.find_one({'_id': ObjectId(id)}, {'_id': 0})
    return render_template('zaiwenling/waimai.html', waimai=waimai)

@mod.route('/waimais/')
def list_waimai():
    waimais = []
    for i in db.waimai.find():
        id = str(i['_id'])
        del i['_id']
        i['objid'] = id

        waimais.append(i)

    return render_template('zaiwenling/waimais.html', waimais=waimais)

@mod.route('/editwaimai/<id>/')
def edit_waimai(id=''):
    waimai = db.waimai.find_one({'_id': ObjectId(id)})

    return render_template('zaiwenling/editwaimai.html', waimai=waimai)

@mod.route('/updatewaimai/', methods=['POST'])
def update_waimai():
    form = request.form
    id = form['_id']
    name = form['name']
    phone = form['phone']
    rate = form['rate']
    tag = form['tag']
    address = form['address']
    ttime = form['ttime']
    valid = form['valid']
    beiz = form['beiz']
    db.waimai.update({'_id': ObjectId(id)}, {'$set': {'name': name, \
        'phone': phone, 'rate': rate, 'tag': tag, \
        'address': address, 'ttime': ttime, 'valid': valid, \
        'beiz': beiz}})
    return redirect(url_for('zaiwenling.get_waimai', id=str(id)))

@mod.route('/about/')
def about():
    return render_template('zaiwenling/about.html')

@mod.route('/bd/')
def bd():
    return render_template('zaiwenling/bd.html')






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
        msgtype = message.get('MsgType', '')

        s = '''
感谢您关注“在温岭”官方微信[愉快]

回复相应数字即可接收相关资讯
0、微信首页
1、今日新闻
2、音乐推荐
3、时尚潮流
4、汽车资讯
5、2048
6、电影资讯
7、糗事百科
8、外卖信息
9、招聘求职
（输入资讯拼音首字母亦可查询，例如您需查询"今日新闻"，你只需输入"jrxw"就好)

在温岭，让我们融入您的生活
            '''

        r = ''

        if Follower.query.filter_by(wxid=ToUserName, openid=FromUserName).count() == 0:
            add_follower(ToUserName, FromUserName, CreateTime, CreateTime)
        else:
            update_follower(ToUserName, FromUserName, CreateTime)

        if msgtype == 'event' and message.get('Event', '') == 'subscribe':
            r = reply('text', s, ToUserName, FromUserName)
        elif msgtype == 'event' and message.get('Event', '') == 'unsubscribe':
            pass
        elif msgtype == 'text':
            content = message.get('Content', '')
            if content == '0' or content == 'wxsy':
                r = reply('news', [{'title':'在温岭', 'description':'在温岭--微信首页','picUrl':'http://zhufwechat.qiniudn.com/qrcode_for_gh_9962cf5ce8a4_430%20(1).jpg','url':'http://wei3h.com/zaiwenling'}], ToUserName, FromUserName)
            elif content == '1' or content == 'jrxw':
                r = reply('news', [{'title':'今日新闻', 'description':'','picUrl':'http://zhufwechat.qiniudn.com/jrxw.png','url':'http://zj.qq.com/'}], ToUserName, FromUserName)
            elif content == '2' or content == 'yytj':
                from sqlalchemy import func
                music = Music.query.order_by(func.random()).first()
                r = reply('news', [{'title':'音乐推荐', 'description':music.music_title + ' by ' + music.music_artist,'picUrl':music.music_pic,'url':'http://wei3h.com/zaiwenling/music/' + str(music.id)}], ToUserName, FromUserName)
            elif content == '4' or content == 'qczx':
                r = reply('news', [{'title':'汽车资讯', 'description':'','picUrl':'http://x.autoimg.cn/news/index/img/20110801/logo_new.png','url':'http://m.autohome.com.cn/'}], ToUserName, FromUserName)
            elif content == '5' or content == '2048':
                r = reply('news', [{'title':'2048', 'description':'','picUrl':'http://zhufwechat.qiniudn.com/image_2049.png','url':'http://wei3h.com/games/2048/'}], ToUserName, FromUserName)
            elif content == '6' or content == 'dyzx':
                r = reply('news', [{'title':'电影资讯', 'description':'最新影讯','picUrl':'http://img31.mtime.cn/mg/2014/03/27/191709.88829508.jpg','url':'http://m.mtime.cn/'}], ToUserName, FromUserName)
            elif content == '7' or content == 'qsbk':
                r = reply('news', [{'title':'糗事百科', 'description':'天王盖地虎, 小鸡炖磨菇','picUrl':'http://static.qiushibaike.com/css/img/web_logo.png','url':'http://www.qiushibaike.com/'}], ToUserName, FromUserName)
            elif content == '8' or content == 'wmxx':
                r = reply('text', 'http://wei3h.com/zaiwenling/waimais/', ToUserName, FromUserName)
            else:
                r = reply('text', '该功能正在测试中…', ToUserName, FromUserName)
        else:
            r = reply('text', s, ToUserName, FromUserName)

        response = make_response(r)
        response.content_type = 'application/xml'
        return response


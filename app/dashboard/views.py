# -*- coding: utf-8 -*-

import datetime
import os
import hashlib
from werkzeug.utils import secure_filename

from flask import Blueprint, request, current_app, render_template, flash, g, session, redirect, url_for, abort
from ..utils.user import get_current_user, require_login
from ..utils.wxuser import get_current_wxuser, login_wxuser

from app import db as mdb

from app.dashboard.models import Filepage

from app.wechat.forms import AddWxuserForm
from app.wechat.models import Wxuser, AccountAndWxuser


mod = Blueprint('dashboard', __name__, url_prefix='/dashboard')

from pymongo import MongoClient
from bson.objectid import ObjectId
conn = MongoClient(host='localhost', port=5430)
db = conn.test

@mod.before_request
def before_request():
    g.user = get_current_user()
    g.wxuser = get_current_wxuser()

@mod.route('/')
@mod.route('/index/')
@require_login
def index():
    form = AddWxuserForm(request.form)
    wxusers = Wxuser.query.from_statement('select * from wechat_wxuser where id in (select wxuser_id from rel_account_wxuser where account_id = %d)' % g.user.id)
    return render_template('dashboard/index.html', today=datetime.date.today(), form=form, wxusers=wxusers)

@mod.route('/wxuser/<id>/home')
@require_login
def wxuser_dashboard(id):
    wxuser = Wxuser.query.get(id)
    login_wxuser(wxuser)
    return render_template('dashboard/dashboard.html', wxuser=wxuser)

@mod.route('/wxuser/<id>/function/subscribe')
@require_login
def wxuser_function_subscribe(id):
    return render_template('dashboard/function_subscribe.html', wxuser=g.wxuser)

@mod.route('/wxuser/function/text')
@require_login
def wxuser_function_text():
    functiontexts = []
    for i in db.reply.find({'wxuser_id': g.wxuser.id, 'msgtype': 'text', 'keyword': {'$ne': 'pdlerfzahufletn'}}):
        id = str(i['_id'])
        del i['_id']
        i['_id'] = id
        functiontexts.append(i)
    return render_template('dashboard/function_text.html', wxuser=g.wxuser, functiontexts=functiontexts)

@mod.route('/addfunctiontext/', methods=['GET', 'POST'])
@require_login
def add_functiontext():
    form = request.form

    wxuser_id = g.wxuser.id
    wxid = g.wxuser.wxid
    keyword = form['keyword']
    ptype = form['ptype']
    content = form['content']
    created = str(datetime.date.today())

    d = {'wxuser_id': wxuser_id, 'wxid': wxid, 'keyword': keyword,
        'ptype': ptype, 'created': created, 'msgtype': 'text', 'content': content}

    if db.reply.find_one({'keyword': keyword, 'wxid': wxid}):
        flash('有重复关键字 ', 'danger')
        return redirect(url_for('dashboard.wxuser_function_text', id=g.wxuser.id))

    if request.method == 'POST':

        db.reply.insert(d)

        flash('添加成功 ', 'success')
        return redirect(url_for('dashboard.wxuser_function_text', id=g.wxuser.id))
    return render_template('dashboard/add_functiontext.html', form=form, wxuser=g.wxuser)

@mod.route('/editfunctiontext/<id>', methods=['GET', 'POST'])
@require_login
def edit_functiontext(id=''):
    functiontext = db.reply.find_one({'_id': ObjectId(id)}, {'_id': 0})

    if functiontext is None:
        abort(404)

    if request.method == 'POST':

        form = request.form

        keyword = form['keyword']
        ptype = form['ptype']
        content = form['content']

        if len([i for i in db.reply.find({'keyword': keyword, 'wxuser_id': g.wxuser.id, '_id': {'$ne': ObjectId(id)}})]) > 0:
            flash('有重复关键字, 无法修改 ', 'danger')
            return redirect(url_for('dashboard.wxuser_function_text', id=g.wxuser.id))


        db.reply.update({'_id': ObjectId(id)}, {'$set': {'keyword': keyword, \
        'ptype': ptype, 'content': content}})

        flash('修改成功 ', 'success')
        return redirect(url_for('dashboard.wxuser_function_text', id=g.wxuser.id))
    return render_template('dashboard/add_functiontext.html', wxuser=g.wxuser, functiontext=functiontext)

@mod.route('/delfunctiontext/<id>', methods=['GET', 'POST'])
@require_login
def del_functiontext(id=''):
    db.reply.remove({'_id': ObjectId(id)})
    flash('删除成功 ', 'success')
    return redirect(url_for('dashboard.wxuser_function_text', id=g.wxuser.id))

@mod.route('/wxuser/function/default', methods=['POST', 'GET'])
@require_login
def wxuser_function_default():
    functiontext = db.reply.find_one({'wxuser_id': g.wxuser.id, 'keyword': 'pdlerfzahufletn'})

    if request.method == 'POST':
        form = request.form

        keyword = 'pdlerfzahufletn'
        ptype = form['ptype']
        content = form['content']

        db.reply.update({'wxuser_id': g.wxuser.id, 'keyword': keyword}, {'$set': {'wxuser_id': g.wxuser.id, 'wxid': g.wxuser.wxid, 'keyword': keyword,
        'ptype': ptype, 'created': str(datetime.date.today()), 'msgtype': 'text', 'content': content}}, upsert = True)

        flash('保存成功 ', 'success')
        return redirect(url_for('dashboard.wxuser_function_default'))

    return render_template('dashboard/add_functiontext.html', wxuser=g.wxuser, functiontext=functiontext)

@mod.route('/filepages/pics/')
@require_login
def filepage_pics():
    pics = Filepage.query.filter_by(ptype='pic', account_id=g.user.id).all()
    return render_template('dashboard/filepage_pics.html', wxuser=g.wxuser, pics=pics)

@mod.route('/filepages/delpic/<id>')
def del_filepages_pic(id):
    filepage = Filepage.query.get(id)
    mdb.session.delete(filepage)
    mdb.session.commit()
    flash('删除成功 ', 'success')
    return redirect(url_for('dashboard.filepage_pics'))

@mod.route('/weshop/index/settings', methods=['GET', 'POST'])
@require_login
def weshop_index_settings():
    shop = db.shop.find_one({'wxuser_id': g.wxuser.id})

    if request.method == 'POST':

        form = request.form

        title = form['title']

        keyword = form['keyword']
        # ptype = 'news'

        description = form['description']
        picurl = form['picurl']


        db.shop.update({'wxuser_id': g.wxuser.id}, {'$set': {'wxuser_id': g.wxuser.id, 'title': title,\
             'keyword': keyword, 'description': description, 'picurl': picurl, \
             'created': str(datetime.date.today())}}, upsert = True)

        flash('保存成功 ', 'success')
        return redirect(url_for('dashboard.weshop_index_settings'))

    return render_template('dashboard/weshop_index_settings.html', wxuser=g.wxuser, shop=shop)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

@mod.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            ptype = '0'
            if filename.rsplit('.', 1)[1] in ['bmp', 'png', 'jpeg', 'jpg', 'gif']:
                ptype = 'pic'

            file.save(os.path.join(current_app.config['UPLOAD_FOLDER']+'/'+ptype, '_' + str(g.user.id) + '_' + filename))

            filepage = Filepage(ptype=ptype, filename=filename, url='/static/uploads/' + ptype + '/_' + str(g.user.id) + '_' + filename)
            filepage.save()
            flash('上传成功 ', 'success')
            return redirect(url_for('dashboard.filepage_pics'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


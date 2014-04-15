# -*- coding: utf-8 -*-

from flask import make_response

from api import *

import MySQLdb, time

t = int(time.time()) - 1272500

conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='123', db='test')
cur = conn.cursor()

cur.execute('select openid from wechat_follower where wxid="gh_9962cf5ce8a4" and last_active_time > %d' % t)

openids = [i[0] for i in cur.fetchall()]

for i in openids:
    print reply('text', '朱峰', 'gh_9962cf5ce8a4', i)
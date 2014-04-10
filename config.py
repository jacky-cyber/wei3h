# -*- coding: utf-8 -*-

import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

ADMINS = frozenset(['zhufeng9282@163.com'])

# base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
SECRET_KEY = 'uyGpSjgfS4+KdfIj1u4LKxUqe0WS7UuArpM3r8dzJQA='
PASSWORD_SECRET = 'aJJOvVwnT72ywBbRtiCMfbXXQeKIj0tqiT6s4jKtyOg='

SQLALCHEMY_DATABASE_URI = 'mysql://root:123@localhost:3306/test?charset=utf8'
DATABASE_CONNECT_OPTIONS = {}

UPLOAD_FOLDER = '/Users/zhufeng/codes/wei3h/app/static/uploads'
ALLOWED_EXTENSIONS = set(['bmp', 'png', 'jpeg', 'jpg', 'gif', 'mp3', 'wma', 'wav', 'amr'])

THREADS_PER_PAGE = 8

CSRF_ENABLED = True
CSRF_SESSION_KEY = 'iggAEy3qSZ6EV/8EuJg7Dr/yYnmgfU+ykAG/qRzirug='

RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
RECAPTCHA_OPTIONS = {'theme': 'white'}
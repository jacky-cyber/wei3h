# -*- coding: utf-8 -*-

import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

ADMINS = frozenset(['zhufeng9282@163.com'])
SECRET_KEY = '+\xfb\x14r\xfb\xacV\x8a\x98`\x8f\xdb\x9c\xdc\x7f\xe1\x97\x9d\xd3~q5\xea\x82'

SQLALCHEMY_DATABASE_URI = 'mysql://root:123@localhost:3306/test?charset=utf8'
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED = True
CSRF_SESSION_KEY = 'Ow(hV\x90\xb2\x0fhU$9H\xd9\x9ap\xe0\x0b\xea>\x16\x08{\xd9'

RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
RECAPTCHA_OPTIONS = {'theme': 'white'}
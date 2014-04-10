# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, SelectField
from wtforms.validators import Required

from app.weshop.models import Shop

class ShopForm(Form):
    title = TextField(u'官网标题', [Required()])

    def save(self):
        shop = Shop(**self.data)
        shop.save()
        return shop

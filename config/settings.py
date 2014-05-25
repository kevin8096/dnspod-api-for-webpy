#!/usr/bin/env python
# coding: utf-8
import web
import os

urls = (
    '/', 'Index',
    '/login', 'Login',
    '/list', 'List',
    '/logout','Logout',
    '/add','AddDomian',
    '/deldomain','DelDomain',
    '/records','Records',
    '/recordAdd','RecordAdd'
)
web.template.Template.globals['r'] = web.template.render(os.path.join(os.path.dirname(__file__), 'templates/'))

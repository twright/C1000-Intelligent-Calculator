#!/usr/bin/env python
__author__ = 'Tom Wright <tom.tdw@gmail.com>'
# Copyright 2012 Thomas Wright <tom.tdw@gmail.com>
# This file is part of C1000 Intelligent Calculator.
#
# C1000 Intelligent Calculator is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# C1000 Intelligent Calculator is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# C1000 Intelligent Calculator.  If not, see <http://www.gnu.org/licenses/>.

import cherrypy
import re
import json
import sx.pisa3 as pisa
from os.path import abspath

from cas.core import StrWithHtml
from calculator import Calculator


class Root:

    @cherrypy.expose
    def index(self):
        ''' The main page of the web interface. '''
        cherrypy.response.headers['Content-type'] = 'text/html'
        return cherrypy.lib.static.serve_file(abspath('webui/index.html'))

    @cherrypy.expose
#    @cherrypy.tools.json_out(on = True)
    def calculate(self, question=None):
        ''' Return answer to the get/post value question via json in
         answer. '''
        cherrypy.response.headers['Content-type'] = 'application/json'
        calc = ''
        if 'workings' not in cherrypy.session:
            cherrypy.session['workings'] = ''
        if 'calc' not in cherrypy.session:
            calc = Calculator()
            calc.set_precision(3)
            cherrypy.session['calc'] = calc
        else:
            calc = cherrypy.session['calc']

        ans = calc.evaluate(question)
        strippedans = ''
        # TODO: Make general
        if isinstance(ans, StrWithHtml):
            ans = re.sub(r'c:/users/.*/appdata/local/temp/', r'/tmp/',
                ans.html, 100)
            strippedans = re.sub('[ ]?style=".*"', '', ans, 100)
            strippedans = re.sub('</?canvas[^>]*>', '', strippedans, 100)
            strippedans = re.sub('svg', 'png', strippedans, 100)
        else:
            ans = '\n'.join(map(lambda a: '<p>' + a + '</p>',
                re.split(r"\n", ans)))
        cherrypy.session['workings'] += ('<div style="page-break-after">'
            + '<h4 style="-pdf-keep-with-next">{}'
            + '</h4>\n<div>{}\n</div></div>\n').format(question, strippedans)
        return json.dumps({'answer': ans})

    @cherrypy.expose
    def workings(self):
        from StringIO import StringIO
#        filename = gen_file_name('workings','.pdf')
        data = '''
        <!doctype html>
        <head>
            <title>Workings</title>
        </head>
        <body>
            {}
        </body>
        '''.format(cherrypy.session['workings'])
        result = StringIO()
        pdf = pisa.CreatePDF(StringIO(data), result, '/')
        if pdf.err:
            return 'A conversion error occured'
        else:
            cherrypy.response.headers['content-type'] = 'application/pdf'
            return result.getvalue()


def start_webui():
    from tempfile import gettempdir
    ip = '127.0.0.1'

    conf = {
        'global': {'server.socket_host': '0.0.0.0',
            'engine.autoreload_on': False},
        '/': {'tools.sessions.on': True, 'tools.sessions.timeout': 90},
        '/help': {'tools.staticdir.on': True,
            'tools.staticdir.dir': abspath('help')},
        '/js': {'tools.staticdir.on': True,
            'tools.staticdir.dir': abspath('webui/js')},
        '/css': {'tools.staticdir.on': True,
            'tools.staticdir.dir': abspath('webui/css')},
        '/images': {'tools.staticdir.on': True,
            'tools.staticdir.dir': abspath('images')},
        '/tmp': {'tools.staticdir.on': True,
            'tools.staticdir.dir': gettempdir(),
            "tools.staticdir.content_types": {'svg': 'image/svg+xml'}}}
    print('Webui running on http://{}:8080/'.format(ip))
    cherrypy.quickstart(Root(), '/', config=conf)

if __name__ == "__main__":
    start_webui()

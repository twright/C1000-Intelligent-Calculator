#!/usr/bin/env python3.1
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

import cherrypy
from cas.core import StrWithHtml
from calculator import Calculator
import re

class Root:
    @cherrypy.expose
    @cherrypy.tools.json_out(on = True)
    def calculate(self, question=None):
        ''' Return answer to the get/post value question via jquery in answer. '''
        calc = ''
        if 'calc' not in cherrypy.session:
            calc = Calculator()
            calc.set_precision(3)
            cherrypy.session['calc'] = calc
        else:
            calc = cherrypy.session['calc']

        ans = calc.evaluate(question)
        # TODO: Make general
        if isinstance(ans, StrWithHtml):
            ans = re.sub(r'c:/users/.*/appdata/local/temp/', r'/tmp/', ans.html, 100)
        else:
            ans = '\n'.join(map (lambda a: '<p>'+a+'</p>', re.split(r"\n", ans)))
        return { 'answer' : ans }

    @cherrypy.expose
    def index(self):
        ''' The main page of the web interface. '''
        return '''
<!doctype html>
<head>
    <title>C1000 Intelligent Calculator</title>
    <link rel='stylesheet' href='style' />
    <script src='jquery'></script>
    <script type="text/javascript">
        function add_result(a, q) {
            q = q || document.getElementById('question').value
            document.getElementById('answers').style.display = ''
            document.getElementById('answers').innerHTML = '<h4 class="question">' + q + '</h4>' + '<p>' + a + '</p>' + document.getElementById('answers').innerHTML
        }

        function calculate(x) {
            x = x || document.getElementById('question').value
            $.getJSON('calculate', {question : x}, function(data) {
                add_result( data.answer, x );
            })
        }
    </script>
</head>
<body>
    <h1>C1000 Intelligent Calculator</h1>
    <div class='center'>
        <input onchange='calculate()' id='question' class='input'></input>
        <div id='answers' class='results' style='display : none'></div>
        <p class='info'><a href='help/index.html' target='_blank'>help</a></p>
    </div>
</body>
        '''

    @cherrypy.expose
    def style(self):
        ''' CSS stylesheet. '''
        cherrypy.response.headers['Content-type'] = 'text/css'
        return '''
h1 {
    font-family : Ubuntu, 'Droid Sans';
    text-align: center;
    margin-bottom : 1pt;
}
body {
    font-family : Ubuntu, 'Droid Sans';
    padding-left : 0;
    padding-right : 0;
}
.input {
    font-family : Ubuntu, 'Droid Sans';
    font-size : 15pt;
    text-align : center;
    width : 100%;
    height : 30pt;
    margin-bottom: 10pt;
    border-style : solid;
}
.results {
    margin-left: 0;
    margin-right: 0;
    padding : 10pt 10pt 10pt 10pt;
    border-style : solid;
    border-width : 2px;
    border-radius : 6pt;
    border-color : #7f7f7f;
    background-color : #e5e5e5;
}
.results img {
    max-height: 500px;
    max-width: 500px;
    background-color: rgba(255,255,255,0.7);
    border-radius: 6pt;
}
.center {
    width : 90%;
    padding-top: 10pt;
    padding-bottom: 10pt;
    margin-left : 5%;
    margin-right : 5%;
    margin-bottom : 40pt;
}
.center .info {
    text-align : center;
    font-size : '0.3em'
}
.results h4 {
/*    text-transform : uppercase;
    margin-bottom : 0; */
    margin-top : 10pt;
    margin-bottom : -10pt;
/*    padding-bottom : 0; */
    clear : none;
}
.results p {
    text-indent : 15pt;
}
        '''

    @cherrypy.expose
    def jquery(self):
        ''' Provide the JQuery JavaScript library. '''
        cherrypy.response.headers['Content-type'] = 'text/javascript'
        with open('jquery-1.4.4.min.js', 'r') as f:
            return f.read()

def start_webui():
    from os.path import abspath
    from tempfile import gettempdir
#    import socket
#    import re
#    import os
#    ip = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][0]
    ip = '127.0.0.1'
#    tmp = re.sub(r'\\', r'/',
#        gettempdir()[2 if os.name == 'nt' else None:], 100)

    conf = {
        'global' : {'server.socket_host': '192.168.0.2'},
        '/' : {'tools.sessions.on': True, 'tools.sessions.timeout': 90},
        '/help' : {'tools.staticdir.on' : True,
            'tools.staticdir.dir' : abspath('help')},
        '/images' : {'tools.staticdir.on' : True,
            'tools.staticdir.dir' : abspath('images')},
        '/tmp' : {'tools.staticdir.on' : True,
            'tools.staticdir.dir' : gettempdir(),
            "tools.staticdir.content_types" : {'svg' : 'image/svg+xml'}}
    }
    print('Webui running on http://{}:8080/'.format(ip))
    cherrypy.quickstart(Root(), '/', config=conf)

if __name__ == "__main__":
    start_webui()


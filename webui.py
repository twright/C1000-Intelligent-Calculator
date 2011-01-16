#!/usr/bin/env python3.1
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

import cherrypy
from cherrypy.process.plugins import Daemonizer
from cas.core import StrWithHtml
from calculator import Calculator
import re
import json
import sx.pisa3 as pisa
from misc import gen_file_name

class Root:
    @cherrypy.expose
#    @cherrypy.tools.json_out(on = True)
    def calculate(self, question=None):
        ''' Return answer to the get/post value question via jquery in answer. '''
#        cherrypy.response.headers['Content-type'] = 'application/javascript+json'
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
        # TODO: Make general
        if isinstance(ans, StrWithHtml):
            ans = re.sub(r'c:/users/.*/appdata/local/temp/', r'/tmp/', ans.html, 100)
        else:
            ans = '\n'.join(map (lambda a: '<p>'+a+'</p>', re.split(r"\n", ans)))
        cherrypy.session['workings'] += '<div style="page-break-after"><h4 style="-pdf-keep-with-next">{}</h4>\n<div>{}\n</div></div>\n'.format(question,re.sub('[ ]?style=".*"', '', ans, 100))
        return json.dumps({ 'answer' : ans })

    @cherrypy.expose
    def index(self):
        ''' The main page of the web interface. '''
        return '''
<!doctype html>
<head>
    <title>C1000 Intelligent Calculator</title>
    <link rel='stylesheet' href='style' />
</head>
<body>
    <h1>C1000 Intelligent Calculator</h1>
    <div class='center'>
        <div contentEditable='True' onkeyup='keypress()' id='question' class='input' type='text'></div>
        
        <div id='answers' class='results' style='display : none'></div>
        <p class='info'><a href='help/index.html' target='_blank'>help</a> |
        <a href='workings'>save workings</a></p>
    </div>
    <script src='stuff/jquery-1.4.4.min.js'></script>
    <script src='stuff/rangy-core.js'></script>
    <script src='stuff/rangy-selectionsaverestore.js'></script>
    <script type="text/javascript">
        function add_result(a, q) {
            q = q || document.getElementById('question').value;
            q = colour_brackets(q); a = colour_brackets(a);
            document.getElementById('answers').style.display = '';
            document.getElementById('answers').innerHTML = '<h4 class="question">' + q + '</h4>' + '<p>' + a + '</p>' + document.getElementById('answers').innerHTML;
        }

        function calculate(x) {
            x = x || document.getElementById('question').innerHTML;
            x = x.replace(/(<([^>]+)>|&[a-z]+;)/ig,'');
            x = x.replace(/[^a-z0-9\\(\\) +\\-\\*\\/\\|\\=\\:\\[\\]\\,\\.\\^]+/ig,'');
            $.getJSON('calculate', {question : x}, function(data) {
                add_result( data.answer, x );
            })
        }
        
        // List of possible bracket colours
        var colours = ['#edd400', '#c4a000', '#8ae234', '#73d216',
            '#4e9a06', '#fcaf3e', '#f57900', '#ce5c00', '#729fcf',
            '#3465a4', '#204a87', '#ad7fa8', '#75507b', '#5c3566',
            '#e9b96e', '#c17d11', '#8f5902', '#cc0000', '#babdb6',
            '#888a85', '#555753', '#2e3436'];
        // Randomize the order of the colours
        colours.sort(function(){return Math.random() - 0.5});
            
        function colour_brackets(s) {
            s = s.replace(/<[//]?(br|div|b)[^>]*>/gi,'');
            var i = 0;
            var result = '';
            for (var j in s) {
                if (s[j] == '(') {
                    result += '<b style="color : ' + colours[i] + '">(</b>';
                    i++;
                } else if (s[j] == ')') {
                    i--;
                    result += (i >= 0) 
                        ? ('<b style="color : ' + colours[i] + '">)</b>')
                        : ('<b style="background-color: #a40000; color: white">)</b>');
                } else {
                    result += s[j]
                }
            }
            return result
        }
        
        function keypress() {
            var sel = rangy.saveSelection();
            if (event.keyCode==13) { calculate(); }
            document.getElementById('question').innerHTML 
                = colour_brackets(document.getElementById('question').innerHTML);
            rangy.restoreSelection(sel);
        }
    </script>
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
    vertical-align : middle;
    margin-bottom : 10pt;
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
        if pdf.err: return 'A conversion error occured'
        else:
            cherrypy.response.headers['content-type'] = 'application/pdf'
            return result.getvalue()

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
        'global' : {'server.socket_host': '0.0.0.0',
            'engine.autoreload_on': False},
        '/' : {'tools.sessions.on': True, 'tools.sessions.timeout': 90},
        '/help' : {'tools.staticdir.on' : True,
            'tools.staticdir.dir' : abspath('help')},
        '/stuff' :  {'tools.staticdir.on' : True,
            'tools.staticdir.dir' : abspath('stuff')},
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


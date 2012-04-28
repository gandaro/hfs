#!/usr/bin/env python
# Copyright (c) 2011  Marcel Hellkamp (parts of `showfile' / `static_file')
# Copyright (c) 2011, 2012  Jakob Kramer
# See LICENSE for details

import os

from urllib import url2pathname
from argparse import ArgumentParser
from mimetypes import read_mime_types

from gevent import wsgi
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import Forbidden, NotFound, HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.debug import DebuggedApplication

MIMETYPES = read_mime_types('/etc/mime.types')
FILEDIR = 'files'

def showfile(request, args):
    # `root' is the file directory's absolute pathname
    root = os.path.abspath(FILEDIR) + os.sep
    path = os.path.abspath(os.path.join(root, args['path'].strip('/\\')))

    if not path.startswith(root):
        raise Forbidden()

    elif not os.path.exists(path) or not os.path.isfile(path):
        raise NotFound()

    elif not os.access(path, os.R_OK):
        raise Forbidden()

    mimetype = MIMETYPES.get(os.path.splitext(path)[1].lower(),
                             'application/octet-stream')

    with open(path, 'rb') as f:
        return Response(f.read(), mimetype=mimetype)


URL_MAP = Map([
    Rule('/<path:path>', endpoint=showfile)
])


@Request.application
def application(request):
    urls = URL_MAP.bind_to_environ(request.environ)

    try:
        endpoint, args = urls.match()

        return endpoint(request, args)
    except HTTPException as e:
        return e


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--deploy', action='store_true')
    args = parser.parse_args()

    if args.deploy:
        print 'Serving on port 5432...'

        try:
            wsgi.WSGIServer(('', 5432), application, spawn=None).serve_forever()
        except KeyboardInterrupt:
            pass

    else:
        run_simple('localhost', 8080, DebuggedApplication(application))

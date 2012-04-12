hfs
===

hfs is a very simple file server using HTTP.

You simply drop files in the *files* folder and then they can be accessed by
opening <http://your_ip_or_domain/file.ext>.

Installation
------------

Install the [Werkzeug][1] and [gevent][2] Python modules, then create a folder
called *files*.

[1]: http://werkzeug.pocoo.org
[2]: http://gevent.org/

Notes
-----

If you are using Windows, you should change */etc/mime.types* to *mime.types*,
because

- Windows has no such file
- Windows' *mime.types* is broken.

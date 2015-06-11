🎃 Ichabod

Ichabod is a server process which accepts POSTed HTML and can rasterize
(eg. render images) and evaluate JS in that HTML document. There is a focus
on rendering speed.

This python client makes it easy to issue requests against an ichabod server
running locally or remotely by constructing a client with the parameters used
to run the server and making requests with that client.

Example usage:

```python
from ichabod import IchabodClient

client = IchabodClient()
result = client.rasterize(html='<h1>Hello, world!</h1>', width=105)
print result
# {u'conversion': True,
#  u'convert_elapsed': 2.25,
#  u'errors': None,
#  u'path': u'/tmp/tmptW2WiV.png',
#  u'result': None,
#  u'run_elapsed': 3.181,
#  u'warnings': None}
```

For more information, see [ichabod.org](http://ichabod.org).

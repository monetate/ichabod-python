# -*- coding: utf-8 -*-
"""
🎃 Ichabod

Ichabod is a server process which accepts POSTed HTML and can rasterize
(eg. render images) and evaluate JS in that HTML document. There is a focus
on rendering speed.

This python client makes it easy to issue requests against an ichabod server
running locally or remotely by constructing a client with the parameters used
to run the server and making requests with that client.

Example usage:

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
"""

import requests
import tempfile

DEFAULT_HOST = '127.0.0.1'

DEFAULT_PORT = 9090

DEFAULT_FORMAT = 'png'

DEFAULT_TIMEOUT = 10

RASTERIZATION_JS = "(function() {ichabod.snapshotPage();ichabod.saveToOutput();})()"

def assert_kwarg(kwarg_name):
    def outer(func):
        def inner(*args, **kwargs):
            assert kwarg_name in kwargs, \
                "Keyword argument '{}' must be provided.".format(kwarg_name)
            return func(*args, **kwargs)
        return inner
    return outer

def assert_one_of_kwargs(*kwarg_names):
    def outer(func):
        def inner(*args, **kwargs):
            assert any(kwarg_name in kwargs for kwarg_name in kwarg_names), \
                "Must provide one of these keyword arguments: {}".format(', '.join(kwarg_names))
            return func(*args, **kwargs)
        return inner
    return outer
    

class IchabodClient(object):
    
    def __init__(self, host=None, port=None, timeout=None, check_health=True):
        self.host = host or DEFAULT_HOST
        self.port = port or DEFAULT_PORT
        self.timeout = timeout or DEFAULT_TIMEOUT
        
        if check_health:
            assert self.is_healthy(), "Ichabod not found at {}".format(self.url)
    
    def _make_health_request(self):
        return requests.get('{}health'.format(self.url), timeout=self.timeout)
        
    def _make_request(self, **kwargs):
        return requests.post(self.url, timeout=self.timeout, data=kwargs).json()
    
    def _make_request_with_tempfile(self, **kwargs):
        suffix = '.{}'.format(kwargs.get('format', DEFAULT_FORMAT))
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
            return self._make_request(output=f.name, **kwargs)
    
    @property
    def url(self):
        return 'http://{self.host}:{self.port}/'.format(self=self)
    
    def is_healthy(self):
        try:
            return self._make_health_request().status_code == 200
        except requests.Timeout:
            return False

    @assert_kwarg('js')
    @assert_one_of_kwargs('html', 'url')
    def evaluate(self, width=1, height=1, **kwargs):
        kwargs['js'] = '{}; {}'.format(RASTERIZATION_JS, kwargs['js'])
        if not 'output' in kwargs:
            return self._make_request_with_tempfile(width=width, height=height, **kwargs)
        return self._make_request(width=width, height=height, **kwargs)
    
    @assert_kwarg('html')
    def evaluate_in_html(self, **kwargs):
        return self.evaluate(**kwargs)
        
    @assert_kwarg('url')
    def evaluate_at_url(self, **kwargs):
        return self.evaluate(**kwargs)
    
    @assert_kwarg('width')
    @assert_one_of_kwargs('html', 'url')
    def rasterize(self, output=None, **kwargs):
        if 'output' in kwargs:
            return self._make_request(js=RASTERIZATION_JS, **kwargs)
        return self._make_request_with_tempfile(js=RASTERIZATION_JS, **kwargs)

    @assert_kwarg('html')
    def rasterize_html(self, **kwargs):
        return self.rasterize(**kwargs)
    
    @assert_kwarg('url')
    def rasterize_url(self, **kwargs):
        return self.rasterize(**kwargs)
    

def rasterize(host=None, port=None, timeout=None, **kwargs):
    client = IchabodClient(host=host, port=port, timeout=timeout, check_health=False)
    return client.rasterize(**kwargs)


def evaluate(host=None, port=None, timeout=None, **kwargs):
    client = IchabodClient(host=host, port=port, timeout=timeout, check_health=False)
    return client.evaluate(**kwargs)

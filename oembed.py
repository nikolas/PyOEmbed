
import re
from urllib import urlopen, urlencode
import urllib2
import json


class Error(ValueError): pass
class FormatError(Error): pass
class NoEndpointError(Error): pass
class HTTPError(Error): pass
class UnauthorizedError(HTTPError): pass
class NotFoundError(HTTPError): pass
class NotImplementedError(HTTPError): pass

_http_errors = {
    401: UnauthorizedError,
    404: NotFoundError,
    501: NotImplementedError,
}


class Endpoint(object):
    
    def __init__(self, endpoint, url=None):
        self.endpoint = endpoint
        self.url = url
    
    def __repr__(self):
        return '<Endpoint:%s>' % self.endpoint
    
    def __str__(self):
        return self.endpoint
    
    def lookup(self, url=None, **kwargs):
        if kwargs.setdefault('format', 'json') not in ('json', 'xml'):
            raise FormatError('unknown format %r' % kwargs['format'])
        body = self.lookup_raw(url, **kwargs)
        if body is None:
            return
        if kwargs['format'] == 'json':
            return json.loads(body)
        return body

    def lookup_raw(self, url=None, **kwargs):       
        url = url or self.url
        if url is None:
            raise Error('must specify url')
        kwargs['url'] = url
        request_url = (self.endpoint % kwargs) + '?' + urlencode(kwargs)
        try:
            request = urllib2.urlopen(urllib2.Request(request_url, headers={
                'User-Agent': 'Python/oEmbed'
            }))
        except urllib2.HTTPError as request:
            pass
        code = request.getcode()
        if code == 200:
            return request.read()
        raise _http_errors.get(code, HTTPError)(code, request_url)


class Consumer(object):
    
    def __init__(self, providers=None):
        self.providers = []
        for scheme, endpoint in (providers or []):
            self.add_provider(scheme, endpoint)
    
    def add_provider(self, scheme, endpoint):
        scheme = scheme.replace('.', r'\.').replace('*', '.*')
        scheme = scheme.replace('://', r'://(www\.)?')
        scheme = re.compile(r'^%s$' % scheme)
        self.providers.append((scheme, endpoint))
    
    def find_endpoint(self, url):
        for scheme, endpoint in self.providers:
            if scheme.match(url):
                return Endpoint(endpoint, url)
    
    def lookup(self, url, **kwargs):
        endpoint = self.find_endpoint(url)
        if not endpoint:
            raise NoEndpointError('no endpoint for %r' % url)
        return endpoint.lookup(url, **kwargs)



if __name__ == '__main__':
    
    from pprint import pprint
    
    consumer = Consumer([
        ('http://flickr.com/*', 'http://www.flickr.com/services/oembed/'),
        ('http://vimeo.com/*', 'http://www.vimeo.com/api/oembed.%(format)s'),
        ('http://youtube.com/watch*', 'http://www.youtube.com/oembed'),
    ])
    #pprint(consumer.lookup('http://vimeo.com/7636406'))
    #pprint(consumer.lookup('http://www.flickr.com/photos/xdjio/226228060/'))
    
    data = consumer.lookup('http://www.flickr.com/photos/mikeboers/5513981190/')
    pprint(data)

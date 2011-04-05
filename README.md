PyOEmbed
=========

Yet another Python implementation of oEmbed consumers.

Usage Example
--------------

    from oembed import Consumer
    from pprint import pprint
    
    consumer = Consumer([
        ('http://flickr.com/*', 'http://www.flickr.com/services/oembed/'),
        ('http://vimeo.com/*', 'http://www.vimeo.com/api/oembed.%(format)s'),
        ('http://youtube.com/watch*', 'http://www.youtube.com/oembed'),
    ])

    data =  consumer.lookup('http://www.flickr.com/photos/mikeboers/5513981190/')
    pprint(data)
    
returns:

    {u'author_name': u'Mike Boers',
     u'author_url': u'http://www.flickr.com/photos/mikeboers/',
     u'cache_age': 3600,
     u'height': u'273',
     u'provider_name': u'Flickr',
     u'provider_url': u'http://www.flickr.com/',
     u'title': u'Emergency Lighting',
     u'type': u'photo',
     u'url': u'http://farm6.static.flickr.com/5218/5513981190_815b89349a.jpg',
     u'version': u'1.0',
     u'width': u'500'}


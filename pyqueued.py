# coding: utf-8

import os
import requests
import json

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

def parse_location(location):
    """ Return hostport, queue, id from url. """
    result = urlparse(location)
    queue, id = result.path.strip('/').split('/')
    return result.netloc, queue, id

class Client:
    """ A client object. """

    def __init__(self, host='localhost', port=5353):
        self.host = host
        self.port = port

    def queue_url(self, queue):
        """ Get the URL to a queue. """
        return "http://{0}:{1}/{2}".format(self.host, self.port, queue)

    def enqueue(self, queue, msg):
        """ Enqueue a message on a given queue. """
        r = requests.post(self.queue_url(queue), data=msg)
        if not r.status_code == 201:
            raise RuntimeError("enqueue failed: %s" % r)
        return r.headers['Location']

    def dequeue(self, queue, wait=None, timeout=None):
        """ Dequeue a message on a given queue. """
        params = dict([(k, v) for k, v in (('wait', wait), ('timeout', timeout)) if v is not None])
        r = requests.post(os.path.join(self.queue_url(queue), 'dequeue'), params=params)
        if not r.status_code == 200:
            raise RuntimeError("dequeue failed: %s" % r)
        return r.text, r.headers['Location']

    def complete(self, queue, id):
        """ Remove an item from a queue. """
        r = requests.delete(os.path.join(self.queue_url(queue), id))
        if not r.status_code == 204:
            raise RuntimeError("complete failed: %s" % r)

    def get(self, queue, id):
        r = requests.get(os.path.join(self.queue_url(queue), id))
        if not r.status_code == 200:
            raise RuntimeError("get failed: %s" % r)
        return r.text

    def stats(self, queue):
        r = requests.get(self.queue_url(queue))
        if not r.status_code == 200:
            raise RuntimeError("stats failed: %s" % r)
        return json.loads(r.text)

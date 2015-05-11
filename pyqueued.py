# -*- coding: utf-8 -*-

import json
import os
import requests

class Client:
    """
    A Queued client object.
    """

    def __init__(self, host='localhost', port=5353):
        self.host = host
        self.port = port

    def queue_url(self, queue):
        """
        Get the URL to a queue.
        """
        return "http://{0}:{1}/{2}".format(self.host, self.port, queue)

    def enqueue(self, queue, msg):
        """
        Enqueue a message on a given queue.
        """
        r = requests.post(self.queue_url(queue), data=msg)
        if not r.status_code == 201:
            raise RuntimeError("enqueue failed: %s, %s" % (r, r.text))
        return r.headers['Location']

    def dequeue(self, queue, wait=None, timeout=None):
        """
        Dequeue a message on a given queue.
        """
        params = dict([(k, v) for k, v in (('wait', wait), ('timeout', timeout)) if v is not None])
        r = requests.post(os.path.join(self.queue_url(queue), 'dequeue'), params=params)
        if not r.status_code == 200:
            raise RuntimeError("dequeue failed: %s" % r)
        return r.text, r.headers['Location']

    def complete(self, queue, id):
        """
        Remove an item from a queue, given its id.
        """
        r = requests.delete(os.path.join(self.queue_url(queue), str(id)))
        if not r.status_code == 204:
            raise RuntimeError("complete failed: %s, %s" % (r, r.text))

    def complete_by_url(self, url):
        """
        Remove an item from a queue, given the items full url.
        """
        queue, id = url.split('/')[-2:]
        hostport = url.split('/')[-3]
        host, port = hostport.split(':')
        if self.host != host or self.port != port:
            raise RuntimeError('client hostport mistmatch')
        r = requests.delete(os.path.join(self.queue_url(queue), id))
        if not r.status_code == 204:
            raise RuntimeError("complete failed: %s, %s" % (r, r.text))

    def get(self, queue, id):
        """
        Get an item by queue and id.
        """
        r = requests.get(os.path.join(self.queue_url(queue), id))
        if not r.status_code == 200:
            raise RuntimeError("get failed: %s, %s" % (r, r.text))
        return r.text

    def stats(self, queue):
        """
        Return stats for a queue.
        """
        r = requests.get(self.queue_url(queue))
        if not r.status_code == 200:
            raise RuntimeError("stats failed: %s, %s" % (r, r.text))
        return json.loads(r.text)

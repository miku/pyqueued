# coding: utf-8

import pyqueued
import random
import requests
import time
import unittest

def random_queue_name():
    return "test_pyqueued_%d" % random.randint(0, 99999999)

class TestClient(unittest.TestCase):

    def test_init(self):
        c = pyqueued.Client()
        self.assertTrue(c is not None)

    def test_enqueue(self):
        Q = random_queue_name()
        c = pyqueued.Client()
        location = c.enqueue(Q, "Hello")
        self.assertTrue(location.startswith(c.queue_url(Q)))
        _, _ = c.dequeue(Q)
        self.assertEquals(c.stats(Q), {u'timeouts': 0, u'depth': 0, u'enqueued': 1, u'dequeued': 1})

    def test_dequeue(self):
        Q = random_queue_name()
        c = pyqueued.Client()
        c.enqueue(Q, "Hello")
        msg, location = c.dequeue(Q)
        self.assertEquals(msg, "Hello")
        self.assertTrue(location.startswith(c.queue_url(Q)))

    def test_dequeue_timeout(self):
        Q = random_queue_name()
        c = pyqueued.Client()
        c.enqueue(Q, "Hello")
        msg, location = c.dequeue(Q, timeout=1)
        self.assertEquals(msg, "Hello")
        self.assertTrue(location.startswith(c.queue_url(Q)))
        id = location.split('/')[-1]
        self.assertEquals(c.stats(Q), {u'timeouts': 0, u'depth': 0, u'enqueued': 1, u'dequeued': 1})
        c.complete(Q, id)
        self.assertEquals(c.stats(Q), {u'timeouts': 0, u'depth': 0, u'enqueued': 1, u'dequeued': 1})

    def test_dequeue_timeout_expire(self):
        Q = random_queue_name()
        c = pyqueued.Client()
        c.enqueue(Q, "Hello")
        msg, location = c.dequeue(Q, timeout=1)
        self.assertEquals(msg, "Hello")
        self.assertTrue(location.startswith(c.queue_url(Q)))
        id = location.split('/')[-1]
        self.assertEquals(c.stats(Q), {u'timeouts': 0, u'depth': 0, u'enqueued': 1, u'dequeued': 1})
        time.sleep(1.1)
        self.assertEquals(c.stats(Q), {u'timeouts': 1, u'depth': 1, u'enqueued': 2, u'dequeued': 1})

    def test_dequeue_wait(self):
        Q = random_queue_name()
        c = pyqueued.Client()
        with self.assertRaises(RuntimeError):
            msg, location = c.dequeue(Q, wait=0.2)

    def test_get_requests(self):
        Q = random_queue_name()
        c = pyqueued.Client()
        location = c.enqueue(Q, "Hello")
        r = requests.get(location)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.text, "Hello")

    def test_get(self):
        Q = random_queue_name()
        c = pyqueued.Client()
        location = c.enqueue(Q, "Hello")
        id = location.split('/')[-1]
        self.assertEquals(c.get(Q, id), "Hello")

    def test_complete_by_url(self):
        Q = random_queue_name()
        c = pyqueued.Client()
        location = c.enqueue(Q, "Hello")
        msg, location = c.dequeue(Q)
        with self.assertRaises(RuntimeError):
            c.complete_by_url(location)

    def test_complete(self):
        Q = random_queue_name()
        c = pyqueued.Client()
        location = c.enqueue(Q, "Hello")
        msg, location = c.dequeue(Q)
        with self.assertRaises(RuntimeError):
            c.complete(*location.split('/')[-2:])

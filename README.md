README
======

Python client for HTTP message queue [Queued](https://github.com/scttnlsn/queued).

Usage
-----

    >>> import pyqueued

Get a client.

    >>> client = pyqueued.Client(host='localhost', port=5353)

Enqueue a message:

    >>> loc = client.enqueue("q", "my message")
    >>> loc
    'http://localhost:5353/q/155'

Get the head of the queue. Without any timeout, the item is marked as completed when dequeued.

    >>> msg, loc = client.dequeue("q")
    >>> msg
    'my message'

THe queue is empty now, so another dequeue will fail:

    >>> msg, loc = client.dequeue("q")
    ...
    RuntimeError: dequeue failed: <Response [404]>

Enqueue another message:

    >>> loc = client.enqueue("q", "my message with timeout")

But dequeue with timeout (given in seconds). If the message is not completed within `timeout`,
it will be enqueued again.

    >>> client.dequeue("q", timeout=2)
    ('my message with timeout', 'http://localhost:5353/q/160')

Now wait 2.1 seconds.

    >>> client.stats("q")
    {'depth': 1, 'dequeued': 3, 'enqueued': 3, 'timeouts': 1}

The has message timed out and has been enqueued again. So we can actually dequeue it once more. But now we
mark it completed in time.

    >>> client.dequeue("q", timeout=2)
    ('my message with timeout', 'http://localhost:5353/q/160')

    >>> client.complete("q", "160")

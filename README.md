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
    >>> print(loc)
    http://localhost:5353/q/155

Get a message. Without any timeout the item is marked as completed when dequeued.

    >>> msg, loc = client.dequeue("q")
    >>> print(msg)
    my message

Queue is empty now, so a new dequeue will fail:

    >>> msg, loc = client.dequeue("q")
    ...
    RuntimeError: dequeue failed: <Response [404]>

Enqueue another message:

    >>> loc = client.enqueue("q", "my message with timeout")

But dequeue with timeout (given in seconds). If the message is not completed within `timeout`,
it will be enqueued again.

    >>> client.dequeue("q", timeout=2)

Now wait 2.1 seconds.

    >>> client.stats("q")
    {'depth': 1, 'dequeued': 3, 'enqueued': 3, 'timeouts': 1}

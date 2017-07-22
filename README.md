# Byth

Small message broker that uses the [stomp.py][stomp] library to interact with
[ActiveMQ][activemq].

I created this prototype to quickly assess the potential integration of ActiveMQ
in the back end layer of a personal project.

## Instructions

Coming soon.

## Examples

### Send a message

```python
>>> import byth.broker
>>> import json
>>>
>>> message = json.dumps({'hello': 'world'})
>>> broker = byth.broker.Broker('stomp://127.0.0.1:61613', 'byth_queue')
>>> broker.connect()
INFO:stomp.py:Attempting connection to host 127.0.0.1, port 61613
INFO:stomp.py:Established connection to host 127.0.0.1, port 61613
INFO:stomp.py:Starting receiver loop
on_connecting 127.0.0.1 61613
on_send STOMP {'accept-version': '1.2', 'host': '127.0.0.1'}
DEBUG:stomp.py:Sending frame: ['STOMP', '\n', 'accept-version:1.2\n', 'host:127.0.0.1\n', '\n', b'\x00']
DEBUG:stomp.py:Received frame: 'CONNECTED', headers={'server': 'ActiveMQ/5.15.0', 'heart-beat': '0,0', 'session': 'ID:DESKTOP:4', 'version': '1.2'}, body=''
on_connected {'server': 'ActiveMQ/5.15.0', 'heart-beat': '0,0', 'session': 'ID:DESKTOP:4', 'version': '1.2'}
>>>
>>> broker.push(message)
on_send SEND {'destination': 'byth_queue', 'content-length': 18} b'{"hello": "world"}'
DEBUG:stomp.py:Sending frame: ['SEND', '\n', 'content-length:18\n', 'destination:byth_queue\n', '\n', b'{"hello": "world"}', b'\x00']
>>>
>>> broker.disconnect()
on_send DISCONNECT {'receipt': '89523745-f88e-499b-aee7-3804efe40974'}
DEBUG:stomp.py:Sending frame: ['DISCONNECT', '\n', 'receipt:89523745-f88e-499b-aee7-3804efe40974\n', '\n', b'\x00']
DEBUG:stomp.py:Received frame: 'RECEIPT', headers={'receipt-id': '89523745-f88e-499b-aee7-3804efe40974'}, body=''
on_receipt {'receipt-id': '89523745-f88e-499b-aee7-3804efe40974'}
on_disconnected
INFO:stomp.py:Receiver loop ended
```

### Retrieve a message

```python
>>> import byth.broker
>>>
>>> broker = byth.broker.Broker('stomp://127.0.0.1:61613', 'byth_queue')
>>> broker.connect()
INFO:stomp.py:Attempting connection to host 127.0.0.1, port 61613
INFO:stomp.py:Established connection to host 127.0.0.1, port 61613
INFO:stomp.py:Starting receiver loop
on_connecting 127.0.0.1 61613
on_send STOMP {'accept-version': '1.2', 'host': '127.0.0.1'}
DEBUG:stomp.py:Sending frame: ['STOMP', '\n', 'accept-version:1.2\n', 'host:127.0.0.1\n', '\n', b'\x00']
DEBUG:stomp.py:Received frame: 'CONNECTED', headers={'server': 'ActiveMQ/5.15.0', 'heart-beat': '0,0', 'session': 'ID:DESKTOP:4', 'version': '1.2'}, body=''
on_connected {'server': 'ActiveMQ/5.15.0', 'heart-beat': '0,0', 'session': 'ID:DESKTOP:4', 'version': '1.2'}
>>> 
>>> broker.subscribe()
on_send SUBSCRIBE {'destination': 'byth_queue', 'id': 1, 'ack': 'auto'}
DEBUG:stomp.py:Sending frame: ['SUBSCRIBE', '\n', 'ack:auto\n', 'destination:byth_queue\n', 'id:1\n', '\n', b'\x00']
on_before_message {'content-length': '18', 'expires': '0', 'destination': '/queue/byth_queue', 'subscription': '1', 'priority': '4', 'message-id': 'ID:DESKTOP:5:-1:1:1', 'timestamp': '1500740959704'} {"hello": "world"}
DEBUG:stomp.py:Received frame: 'MESSAGE', headers={'content-length': '18', 'expires': '0', 'destination': '/queue/byth_queue', 'subscription': '1', 'priority': '4', 'message-id': 'ID:DESKTOP:5:-1:1:1', 'timestamp': '1500740959704'}, body='{"hello": "world"}'
on_message {'content-length': '18', 'expires': '0', 'destination': '/queue/byth_queue', 'subscription': '1', 'priority': '4', 'message-id': 'ID:DESKTOP:5:-1:1:1', 'timestamp': '1500740959704'} {"hello": "world"}
>>> broker.pop_message()
['{"hello": "world"}']
>>> 
>>> broker.disconnect()
```

## Dependencies

Coming soon.

## Code metrics

Coming soon.

## License

Copyright (c) 2017 Eduardo Ferreira

The code in this repository is MIT licensed, and therefore free to use as you
please for commercial or non-commercial purposes (see [LICENSE](LICENSE) for
details).

[stomp]: https://github.com/jasonrbriggs/stomp.py
[activemq]: https://activemq.apache.org/

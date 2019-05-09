# Byth

Small message broker in Python 3 that uses the [stomp.py][stomp] library to
interact with [ActiveMQ][activemq].

I created this prototype to quickly assess the potential integration of ActiveMQ
in the back end layer of a personal project.

## Instructions

* Clone the repository

```
$ git clone git@github.com:MulberryBeacon/byth.git
Cloning into 'byth'...
remote: Counting objects: 23, done.
remote: Compressing objects: 100% (18/18), done.
remote: Total 23 (delta 6), reused 17 (delta 4), pack-reused 0
Receiving objects: 100% (23/23), 6.78 KiB | 0 bytes/s, done.
Resolving deltas: 100% (6/6), done.
Checking connectivity... done.
```

* Install with `pip`

```
$ pip install .
Processing /path/to/byth
Collecting stomp.py>=4.1.18 (from byth==0.0.1)
Installing collected packages: stomp.py, byth
  Running setup.py install for byth ... done
Successfully installed byth-0.0.1 stomp.py-4.1.18
```

## Examples

* Send a message

```
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

* Retrieve a message

```
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

## Code metrics

* CLOC

```
http://cloc.sourceforge.net v 1.60  T=0.23 s (8.7 files/s, 1026.6 lines/s)
-------------------------------------------------------------------------------
File                             blank        comment           code
-------------------------------------------------------------------------------
./byth/broker.py                    38            112             65
./setup.py                           2              8             12
-------------------------------------------------------------------------------
SUM:                                40            120             77
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                           2             40            120             77
-------------------------------------------------------------------------------
SUM:                             2             40            120             77
-------------------------------------------------------------------------------
```

* SLOCCount

```
SLOC    Directory       SLOC-by-Language (Sorted)
65      byth            python=65
12      top_dir         python=12
0       byth.egg-info   (none)

Totals grouped by language (dominant language first):
python:          77 (100.00%)

Total Physical Source Lines of Code (SLOC)                = 77
Development Effort Estimate, Person-Years (Person-Months) = 0.01 (0.16)
 (Basic COCOMO model, Person-Months = 2.4 * (KSLOC**1.05))
Schedule Estimate, Years (Months)                         = 0.10 (1.25)
 (Basic COCOMO model, Months = 2.5 * (person-months**0.38))
Estimated Average Number of Developers (Effort/Schedule)  = 0.13
Total Estimated Cost to Develop                           = $ 1,830
 (average salary = $56,286/year, overhead = 2.40).
SLOCCount, Copyright (C) 2001-2004 David A. Wheeler
SLOCCount is Open Source Software/Free Software, licensed under the GNU GPL.
SLOCCount comes with ABSOLUTELY NO WARRANTY, and you are welcome to
redistribute it under certain conditions as specified by the GNU GPL license;
see the documentation for details.
Please credit this data as "generated using David A. Wheeler's 'SLOCCount'."
```

## License

Copyright (c) 2017 Eduardo Ferreira

The code in this repository is MIT licensed, and therefore free to use as you
please for commercial or non-commercial purposes (see [LICENSE](LICENSE) for
details).

[stomp]: https://github.com/jasonrbriggs/stomp.py
[activemq]: https://activemq.apache.org/

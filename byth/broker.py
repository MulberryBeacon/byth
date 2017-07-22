# -*- coding: utf-8 -*-
"""
API to interact with a message broker.
"""

# Module import
# -------------------------------------------------------------------------------------------------
import urllib.parse as parse
import logging
import time
import stomp

# Logger
# -------------------------------------------------------------------------------------------------
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

# Classes
# -------------------------------------------------------------------------------------------------
class MyListener(stomp.ConnectionListener):
    """
    Custom listener to ping the queue for new messages.
    """
    def __init__(self, messages):
        """
        :param buffer:
            The list of messages retrieved from the queue in one sit
        """
        self.buffer = messages

    def on_message(self, headers, body):
        """
        Called by the STOMP connection when a MESSAGE frame is received.
        This method overrides the implementation provided for the stomp.ConnectionListener object.

        :param dict headers:
            a dictionary containing all headers sent by the server as key/value pairs.
        :param body:
            the frame's payload - the message body.
        """
        self.buffer.append(body)


class Broker(object):
    """
    Represents the information needed to establish a connection with a message broker.
    """
    def __init__(self, broker_uri, queue):
        """
        :param broker_uri:
            The address of the message broker
        :param queue:
            The name of the message queue
        """
        # The tuple with the hostname and port of the message broker
        self.host_and_port = self._parse_uri(broker_uri)
        self.queue = queue

        # The stomp.Connection12 instance with the connection to the message broker
        self.connection = None

        # The internal buffer with messages retrieved from the queue. It's managed as a stack,
        # which means that it works as FIFO.
        self.message_buffer = []


    def connect(self):
        """
        Establishes a new connection to the message broker.

        :raises stomp.exception.StompException:
            Common exception class. All specific stomp.py exceptions are subclasses of
            StompException, allowing the library user to catch all current and future library
            exceptions.
        """
        try:
            self.connection = stomp.Connection12([self.host_and_port])
            self.connection.set_listener('PrintingListener', stomp.listener.PrintingListener())
            self.connection.start()
            self.connection.connect(wait=True)
        except stomp.exception.StompException as ex:
            LOGGER.error(ex)
            quit(1)


    def subscribe(self):
        """
        Subscribes to a queue in the message broker.

        :raises stomp.exception.StompException:
            Common exception class. All specific stomp.py exceptions are subclasses of
            StompException, allowing the library user to catch all current and future library
            exceptions.
        """
        try:
            self.connection.set_listener('MyListener', MyListener(self.message_buffer))
            self.connection.subscribe(destination=self.queue, id=1, ack='auto')
            time.sleep(2)
        except stomp.exception.StompException as ex:
            LOGGER.error(ex)
            quit(1)


    def push(self, message):
        """
        Sends a message to the queue.

        :param message:
            The message

        :raises stomp.exception.StompException:
            Common exception class. All specific stomp.py exceptions are subclasses of
            StompException, allowing the library user to catch all current and future library
            exceptions.
        """
        try:
            time.sleep(2)
            self.connection.send(self.queue, message)
        except stomp.exception.StompException as ex:
            LOGGER.error(ex)
            quit(1)


    def disconnect(self):
        """
        Disconnects from the message broker.

        :raises stomp.exception.StompException:
            Common exception class. All specific stomp.py exceptions are subclasses of
            StompException, allowing the library user to catch all current and future library
            exceptions.
        """
        try:
            time.sleep(2)
            self.connection.disconnect()
        except stomp.exception.StompException as ex:
            LOGGER.error(ex)
            quit(1)


    def pop_message(self):
        """
        Retrieves the message at the top of the buffer.

        :rtype:
            object
        :return:
            The first message in the buffer
        """
        return self.pop_messages(1)


    def pop_messages(self, number):
        """
        Retrieves a specific number of messages from the top of the buffer.

        :param number:
            The number of messages to retrieve from the buffer
        :rtype:
            list
        :return:
            A list with the first 'number' messages in the buffer
        """
        return [self.message_buffer.pop(0) for index in range(number) if self.message_buffer]


    def _parse_uri(self, broker_uri):
        """
        Parses a message broker URI to retrieve the hostname and the port.

        As an example, the URI would be something like: 'stomp://127.0.0.1:61613'

        :param broker_uri:
            The broker URI
        :rtype:
            tuple
        :return:
            A tuple with the hostname and the port
        """
        elements = parse.urlparse(broker_uri)
        return (elements.hostname, elements.port)


def fancy_send(broker, message):
    """
    Fancy wrapper that combines several operations to send a message to the message broker.

    :param broker:
        The Broker instance
    :param message:
        The message
    """
    broker.connect()
    broker.push(message)
    broker.disconnect()


def fancy_retrieve(broker, num_messages=1):
    """
    Fancy wrapper that combines several operations to retrieve a message from the message broker.

    :param broker:
        The Broker instance
    :param num_messages:
        The number of messages to retrieve from the queue
    :rtype:
        list
    :return:
        The list of messages kept in the internal message buffer
    """
    broker.connect()
    broker.subscribe()
    messages = broker.pop_messages(num_messages)
    broker.disconnect()
    return messages

# -*- coding: utf-8 -*-
"""
API to interact with a message broker.

WARNING
=======
This file is classified and access to it requires top-level privileges. If you're currently looking
at the code without the proper clearance, please kill yourself now.
"""

# Module import
# -------------------------------------------------------------------------------------------------
from urlparse import urlparse
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

    def on_message(self, headers, message):
        self.buffer.append(message)


class Broker(object):
    """
    Represents the information needed to establish a connection with a message broker.
    """
    def __init__(self, broker_uri, queue):
        """
        :param host_and_port:
            The tuple with the hostname and port of the message broker
        :param queue:
            The message queue
        :param connection:
            The connection to the message broker
        :param message_buffer:
            The stack with messages retrieved from the queue
        """
        self.host_and_port = self.__parse_uri(broker_uri)
        self.queue = queue
        self.connection = None
        # This internal buffer is managed as a stack, which means that it works as FIFO.
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
            LOGGER.error(ex.message)
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
            #self.connection.subscribe(destination=self.queue, id=1, ack='client')
            #self.connection.subscribe(destination=self.queue, id=1, ack='client-individual')
            time.sleep(2)
        except stomp.exception.StompException as ex:
            LOGGER.error(ex.message)
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
            LOGGER.error(ex.message)
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
            LOGGER.error(ex.message)
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


    def __parse_uri(self, broker_uri):
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
        elements = urlparse(broker_uri)
        return (elements.hostname, elements.port)


def fancy_send(broker, message):
    """
    Sends a message to the message broker.

    :param broker:
        The Broker instance
    :param message:
        The message
    """
    broker.connect()
    broker.push(message)
    broker.disconnect()


def fancy_receive(broker, num_messages=1):
    """

    :param broker:
        The Broker instance
    :param num_messages:
        The number of messages to retrieve from the queue
    :rtype:
        ???
    :return:
        ???
    """
    broker.connect()
    broker.subscribe()
    messages = broker.pop_messages(num_messages)
    broker.disconnect()
    return messages

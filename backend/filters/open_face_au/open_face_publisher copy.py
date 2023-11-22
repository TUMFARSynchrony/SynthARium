#!/usr/bin/env python

from time import sleep
import functools
import json
import logging
import pika
import threading
import time
import uuid


class OpenFacePublisher(object):

    """Asynchronous Rpc client."""

    def __init__(self):
        super().__init__()
        # self.daemon = True
        self.is_running = True
        self.response = None
        self.corr_id = None
        self.logger = logging.getLogger("OpenFacePublisher")
        logging.getLogger("pika").setLevel(logging.WARNING)

        #TODO: Initiate connection at the beginning of hub
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                heartbeat=30,
                blocked_connection_timeout=15))

        self.channel = self.connection.channel()
        self.queue_name = "test"
        self.callback_queue = "callback"
        
        try:
            self.channel.queue_declare(queue=self.queue_name, auto_delete=False)
            self.channel.queue_declare(queue=self.callback_queue, auto_delete=False)
            self.logger.debug(f"Binding callback queue: {self.callback_queue}")

        except pika.exceptions.ChannelClosedByBroker as e:
            if "RESOURCE_LOCKED" in str(e):
                 self.logger.debug(f"Queue '{self.callback_queue}' is already declared as exclusive on another connection.")
            else:
                raise
        except Exception as e:
             self.logger.debug(f"Got error '{e}'")

        # # self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response)
        
        # thread = threading.Thread(target=self.connection.process_data_events(time_limit=None))
        # thread.setDaemon(True)
        # thread.start()

    def on_response(self, ch, method, props, body):
        # if self.corr_id == props.correlation_id:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        self.response = json.loads(body)


    def publish(self, message):
        self.response = None
        corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='amq.direct',
            routing_key=self.queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=corr_id,
                ),
                body=message)
        while self.response is None:
            self.connection.process_data_events(time_limit=None)

        return self.response
    
    # def publish(self, message):
    #     self.connection.add_callback_threadsafe(lambda: self._publish(message))

    #     self._logger.debug(f"Received: {self.response}")

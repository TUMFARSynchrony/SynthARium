#!/usr/bin/env python

from time import sleep
import logging
import pika
import threading
import uuid


class OpenFacePublisher():

    """Asynchronous Rpc client."""
    # internal_lock = threading.Lock()
    queue = {}

    def __init__(self):

        self.logger = logging.getLogger("OpenFacePublisher")
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()
        queue_name = "test"
        # try:
        #     # Attempt to declare an exclusive queue
        #     result = self.channel.queue_declare(queue='test', exclusive=True)
        #     print(f"Declared exclusive queue: {queue_name}")
        # except pika.exceptions.ChannelClosedByBroker as e:
        #     if "RESOURCE_LOCKED" in str(e):
        #         print(f"Queue '{queue_name}' is already declared as exclusive on another connection.")
        #         self.channel.queue_bind
        #     else:
        #         raise
        
        self.channel.queue_bind(queue_name, "amq.direct", queue_name)
        self.callback_queue = queue_name
        self.logger.debug(
            f"Declaring queue: {self.callback_queue}"
        )

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None
        # thread = threading.Thread(target=self.process_data_events)
        # thread.setDaemon(True)
        # thread.start()
    
    def process_data_events(self):
        """Check for incoming data events.

        We do this on a thread to allow the flask instance to send
        asynchronous requests.

        It is important that we lock the thread each time we check for events.
        """
        self.channel.basic_consume(queue=self.callback_queue,
                                   on_message_callback=self.on_response, 
                                   auto_ack=False)
        while True:
            with self.internal_lock:
                self.connection.process_data_events(time_limit=None)
                sleep(0.1)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def send(self, message):
        self.response = None
        try:
            self.corr_id = str(uuid.uuid4())
            self.channel.basic_publish(
                exchange='amq.direct',
                routing_key='test',
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                    correlation_id=self.corr_id,
                ),
                body=message)
            self.logger.debug(f"Publishing to OpenFace. Correlation-ID: {self.corr_id}")
        except KeyboardInterrupt:
            print("Detected Keyboard Interrupt. Exiting...")
        return self.response
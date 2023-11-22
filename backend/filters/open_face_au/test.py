# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205

import threading
from time import sleep
import uuid
from pika import ConnectionParameters, BlockingConnection, PlainCredentials, BasicProperties


class Publisher(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.daemon = True
        self.is_running = True
        self.name = "Publisher"
        self.queue = "downstream_queue"

        credentials = PlainCredentials("guest", "guest")
        parameters = ConnectionParameters("localhost", credentials=credentials)
        self.connection = BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, auto_delete=True)

        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.on_response)

    def on_response(self, ch, method, props, body):
        print(f"Response '{body}'")

    def run(self):
        while self.is_running:
            self.connection.process_data_events(time_limit=1)

    def _publish(self, message):
        corr_id = str(uuid.uuid4())
        self.channel.basic_publish("", self.queue, properties=BasicProperties(
                reply_to=self.queue,
                correlation_id=corr_id,
                ),
                body=message.encode())

    def publish(self, message):
        self.connection.add_callback_threadsafe(lambda: self._publish(message))

    def stop(self):
        print("Stopping...")
        self.is_running = False
        # Wait until all the data events have been processed
        self.connection.process_data_events(time_limit=1)
        if self.connection.is_open:
            self.connection.close()
        print("Stopped")


if __name__ == "__main__":
    publisher = Publisher()
    publisher.start()
    try:
        for i in range(10):
            msg = f"Message {i}"
            print(f"Publishing: {msg!r}")
            publisher.publish(msg)
            sleep(0.3)
    except KeyboardInterrupt:
        publisher.stop()
    finally:
        publisher.join()
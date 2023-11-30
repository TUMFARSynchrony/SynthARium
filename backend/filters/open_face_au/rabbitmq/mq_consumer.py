import asyncio
import functools
import json
import logging
import threading

from .mq_basic import MQBasic
from ..open_face_data_parser import OpenFaceDataParser

# def sync(f):
#     @functools.wraps(f)
#     def wrapper(*args, **kwargs):
#         return asyncio.new_event_loop().run_until_complete(f(*args, **kwargs))

#     return wrapper
 
class MQConsumer(MQBasic):

    queue: dict
    channel_tag: any
    consumer_thread: threading.Thread
    file_writer: OpenFaceDataParser

    def __init__(self, queue_name: str, routing_key: str, exchange_name: str = "amq.direct"):
        super().__init__()
        self.logger = logging.getLogger("MQConsumer")
        self.file_writer = OpenFaceDataParser(routing_key, queue_name)
        self.declare_queue(queue_name=queue_name)
        self.bind_queue(
            exchange_name=exchange_name, queue_name=queue_name, routing_key=routing_key
        )
        self.channel_tag = None
        self.queue = {}
        self.consume_messages(queue=queue_name, callback=self.consume)

    def get_message(self, queue_name: str, auto_ack: bool = False):
        method_frame, header_frame, body = self.channel.basic_get(
            queue=queue_name, auto_ack=auto_ack
        )
        if method_frame:
            self.logger.debug(f"{method_frame}, {header_frame}, {body}")
            return method_frame, header_frame, body
        else:
            self.logger.debug("No message returned")
            return None

    def consume_messages(self, queue, callback):
        self.check_connection()
        self.channel_tag = self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=True
        )
        self.consumer_thread = threading.Thread(target=self.channel.start_consuming)
        self.consumer_thread.start()
        self.consumer_thread.join(0)

    def cancel_consumer(self):
        if self.channel_tag is not None:
            self.channel.basic_cancel(self.channel_tag)
            self.channel_tag = None
        else:
            self.logger.error("Do not cancel a non-existing job")

    # @sync
    async def consume(self, channel, method, properties, body):
        json_body = json.loads(body)
        if (int(properties.correlation_id) % 30 == 0):
            self.queue[properties.correlation_id] = json_body
        self.file_writer.write(properties.correlation_id, json_body)
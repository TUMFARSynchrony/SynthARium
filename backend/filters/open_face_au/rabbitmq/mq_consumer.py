import json
import logging
import threading

from server import Config
from .mq_basic import MQBasic
from ..open_face_data_parser import OpenFaceDataParser

class MQConsumer(MQBasic):

    queue_name: str
    channel_tag: any
    consumer_thread: threading.Thread
    file_writer: OpenFaceDataParser
    result: dict

    def __init__(self, queue_name: str, session_id: str, exchange_name: str = "amq.direct"):
        super().__init__()
        self.logger = logging.getLogger("MQConsumer")
        self.server_config = Config()
        self.result = {}

        filename = queue_name.split(".")[0]
        self.file_writer = OpenFaceDataParser(session_id, filename, self.server_config.openface_au)
        self.declare_queue(queue_name=queue_name)
        self.bind_queue(
            exchange_name=exchange_name, queue_name=queue_name, routing_key=queue_name
        )
        self.channel_tag = None
        self.queue_name = queue_name
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
            self.channel.queue_purge(self.queue_name)
            self.channel.basic_cancel(self.channel_tag)
            self.channel_tag = None
        else:
            self.logger.error("Do not cancel a non-existing job")

    def consume(self, channel, method, properties, body):
        json_body = json.loads(body)
        self.result[int(properties.correlation_id)] = json_body
        self.result = dict(sorted(self.result.items()))
        self.file_writer.write(int(properties.correlation_id), json_body)

    def __del__(self):
        del self.file_writer
        self.cancel_consumer()

import logging
import pika

from typing import Optional
from .mq_basic import MQBasic

class MQPublisher(MQBasic):

    queue_name: str
    routing_key: str
    exchange_name: str
    reply_to: str

    def __init__(self, queue_name: str, routing_key: str, reply_to: Optional[str], exchange_name: str = "amq.direct"):
        super().__init__()
        self.logger = logging.getLogger("MQPublisher")
        self.queue_name = queue_name
        self.routing_key = routing_key
        self.exchange_name = exchange_name
        self.reply_to = reply_to

        self.declare_queue(queue_name=queue_name)
        self.bind_queue(
            exchange_name=exchange_name, queue_name=queue_name, routing_key=routing_key
        )

    def publish(self, body: str, corr_id: Optional[str]):
        properties = None
        if self.reply_to is not None and corr_id is not None:
            properties = pika.BasicProperties(reply_to=self.reply_to, correlation_id=corr_id)
        
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=body,
            properties=properties,
        )
        

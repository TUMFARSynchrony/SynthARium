import logging
import pika
import ssl
import time

from pika.exceptions import AMQPConnectionError
from pika.exceptions import AMQPConnectionError

from server import Config
from .mq_config import MQConfig

class MQBasic:

    config: MQConfig
    parameters: pika.ConnectionParameters
    credentials: pika.PlainCredentials
    connection: pika.BlockingConnection

    def __init__(self):
        self.logger = logging.getLogger("MQBasic")
        logging.getLogger("pika").setLevel(logging.WARNING)

        self.config = MQConfig(Config())

        self._init_connection_parameters()
        self._connect()

    def _connect(self):
        tries = 0
        while True:
            try:
                self.connection = pika.BlockingConnection(self.parameters)
                self.channel = self.connection.channel()
                if self.connection.is_open:
                    break
            except (AMQPConnectionError, Exception) as e:
                time.sleep(5)
                tries += 1
                if tries == 20:
                    raise AMQPConnectionError(e)

    def _init_connection_parameters(self):
        self.credentials = pika.PlainCredentials(self.config.username, self.config.password)
        self.parameters = pika.ConnectionParameters(
            self.config.host,
            int(self.config.port),
            "/",
            self.credentials,
        )
        if self.config.protocol == "amqps":
            # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.set_ciphers("ECDHE+AESGCM:!ECDSA")
            self.parameters.ssl_options = pika.SSLOptions(context=ssl_context)

    def check_connection(self):
        if not self.connection or self.connection.is_closed:
            self._connect()

    def close(self):
        self.channel.close()
        self.connection.close()

    def declare_queue(
        self, queue_name, exclusive: bool = False, max_priority: int = 10
    ):
        self.check_connection()
        self.logger.debug(f"Trying to declare queue({queue_name})...")
        self.channel.queue_declare(
            queue=queue_name,
            exclusive=exclusive
        )

    def declare_exchange(self, exchange_name: str, exchange_type: str = "direct"):
        self.check_connection()
        self.channel.exchange_declare(
            exchange=exchange_name, exchange_type=exchange_type
        )

    def bind_queue(self, exchange_name: str, queue_name: str, routing_key: str):
        self.check_connection()
        self.channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key=routing_key
        )

    def unbind_queue(self, exchange_name: str, queue_name: str, routing_key: str):
        self.channel.queue_unbind(
            queue=queue_name, exchange=exchange_name, routing_key=routing_key
        )
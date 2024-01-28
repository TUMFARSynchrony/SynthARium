from server import Config

class MQConfig():
    host: str
    port: int
    username: str
    password: str
    protocol: str

    def __init__(self, config: Config):
        self.host = config.rabbitmq["host"]
        self.port = config.rabbitmq["port"]
        self.username = config.rabbitmq["username"]
        self.password = config.rabbitmq["password"]
        self.protocol = config.rabbitmq["protocol"]


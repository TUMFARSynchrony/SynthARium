"""Provide Config class"""


from typing import Literal

import json
from os.path import join
from modules import BACKEND_DIR


class Config:
    """Config for experimental hub backend"""

    host: str
    port: int
    environment: Literal["dev", "prod"]

    def __init__(self):
        """Load config from `backend/config.json`.

        Raises
        ------
        ValueError
            If a key in `backend/config.json` is missing or has the wrong type.
        """
        config_path = join(BACKEND_DIR, "config.json")
        config = json.load(open(config_path))

        # Check if keys exist and types are correct.
        data_types = {
            "host": str,
            "port": int,
            "environment": str,  # Literal not supported here, check afterwards.
        }
        for key in data_types.keys():
            if key not in config:
                raise ValueError(
                    f"{key} with type {data_types[key]} is missing in config.json."
                )
            if not isinstance(config[key], data_types[key]):
                raise ValueError(
                    f"{key} must be of type {data_types[key]} in config.json."
                )

        # Special data checks.
        if config["environment"] not in ["dev", "prod"]:
            raise ValueError("'environment' must be 'dev' or 'prod' in config.json.")

        # Load config into this class.
        self.host = config["host"]
        self.port = config["port"]
        self.environment = config["environment"]
        print(f"[CONFIG] successfully loaded config: {self}")

    def __str__(self) -> str:
        """Get string representation of parameters in this Config.

        Format: "host: <host>, port: <port>, environment: <environment>."
        """
        return f"host: {self.host}, port: {self.port}, environment: {self.environment}."

    def __repr__(self) -> str:
        """Get representation of this Config obj.

        Format: "Config(host: <host>, port: <port>, environment: <environment>.)"
        """
        return f"Config({self.__str__})"

"""TODO document"""


from modules.filter_api import FilterAPI


class FilterSubprocessReceiver:
    """TODO document"""

    _filter_api: FilterAPI

    def __init__(self, filter_api: FilterAPI) -> None:
        """TODO document"""
        self._filter_api = filter_api

    async def handle(self, message: dict):
        """TODO document"""
        command = message.get("command")
        data = message.get("data")

        if command is None or data is None:
            return

        match command:
            case "EXPERIMENT_SEND":
                await self._filter_api.experiment_send(
                    data["to"], data["data"], data["exclude"]
                )
            case _:
                # TODO handle unknown command
                pass

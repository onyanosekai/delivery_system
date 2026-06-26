class Driver:
    def __init__(self, driver_id: int, driver_name: str):
        self._driver_id = driver_id
        self._driver_name = driver_name

    @property
    def driver_id(self) -> int:
        return self._driver_id

    @property
    def driver_name(self) -> str:
        return self._driver_name

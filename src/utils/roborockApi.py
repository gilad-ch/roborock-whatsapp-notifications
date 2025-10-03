from roborock import DeviceData, RoborockDockErrorCode
from roborock.version_1_apis import RoborockMqttClientV1
from roborock.web_api import RoborockApiClient
from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv("ROBOROCK_USERNAME")
password = os.getenv("ROBOROCK_PASSWORD")


class RoborockApi:
    def __init__(self):
        self.mqtt_client = None

    async def start(self):
        web_api = RoborockApiClient(username=username)
        user_data = await web_api.pass_login(password=password)
        home_data = await web_api.get_home_data_v2(user_data)
        device = home_data.devices[0]
        product_info = {product.id: product for product in home_data.products}
        device_data = DeviceData(device, product_info[device.product_id].model)
        self.mqtt_client = RoborockMqttClientV1(user_data, device_data)

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

    def _parse_status(self, status):
        dock_error = status.dock_error_status
        return {
            "water_shortage": dock_error == RoborockDockErrorCode.water_empty,
            "dirty_tank_missing": dock_error
            == RoborockDockErrorCode.dirty_tank_latch_open,
            "waste_water_tank_full": dock_error
            == RoborockDockErrorCode.waste_water_tank_full,
            "basin_blocked": dock_error
            == RoborockDockErrorCode.cleaning_tank_full_or_blocked,
        }

    async def get_status(self):
        status = await self.mqtt_client.get_status()
        return self._parse_status(status)

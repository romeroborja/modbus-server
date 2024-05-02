from pymodbus.server import StartTcpServer
from threading import Thread
import logging

logger = logging.getLogger(__name__)

class ModbusServer(Thread):

    def __init__(self, manager: object, ip: str, port: int) -> None:
        super().__init__()
        self.manager = manager
        self.ip = ip
        self.port = port    
    
    def start_modbus_server(self) -> None:
        context = self.manager.get_context()
        logger.info(f'Starting modbus server on {self.ip}:{self.port}')
        StartTcpServer(
            context = context,
            address = (self.ip, self.port)
        )    

    def run(self) -> None:        
        self.start_modbus_server()
import time

from flask import Flask
from web import run_flask
from modbus import ModbusServer
from modbus.modbus_manager import ModbusManager
from database import DatabaseManager
from logger_config import logger_config

def main():
    database_manager = DatabaseManager()
    modbus_manager = ModbusManager(database_manager)
    modbus_server = ModbusServer(
        manager = modbus_manager,
        ip = '0.0.0.0',
        port = 502
    )
    modbus_server.start()
    time.sleep(1)
    run_flask(modbus_manager)

if __name__ == '__main__':
    main()
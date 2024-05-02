import json
import logging
import struct

from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian
from pymodbus.exceptions import ModbusException

logger = logging.getLogger(__name__)

class ModbusManager():

    SLAVE_ID = 0x00
    READ_HOLDING_REGISTERS = 0x03
    WRITE_HOLDING_REGISTERS = 0x10

    def __init__(self, database_manager: object) -> None:
        self.database_manager = database_manager
        self.registers = self._load_registers_from_bbdd()
        self.context = self._create_context()
        self.registers_index = self._create_index()
        self._update_server(self.registers)

    def _encoder_data(self, encoder, value: str, format: str) -> None:
        encoders = {
            "INT8": lambda encoder, value: encoder.add_8bit_int(value),
            "UINT8": lambda encoder, value: encoder.add_8bit_uint(value),
            "INT16": lambda encoder, value: encoder.add_16bit_int(value),
            "UINT16": lambda encoder, value: encoder.add_16bit_uint(value),
            "INT32": lambda encoder, value: encoder.add_32bit_int(value),
            "UINT32": lambda encoder, value: encoder.add_32bit_uint(value),
            "FLOAT16": lambda encoder, value: encoder.add_16bit_float(value),
            "FLOAT32": lambda encoder, value: encoder.add_32bit_float(value),
            "INT64": lambda encoder, value: encoder.add_64bit_int(value),
            "UINT64": lambda encoder, value: encoder.add_64bit_uint(value),
            "FLOAT64": lambda encoder, value: encoder.add_64bit_float(value),
        }
        encoders[format](encoder, int(value))
    
    def _decoder_data(self, decoder, format: str) -> None:        
        decoders = {        
            "INT8": lambda decoder: decoder.decode_8bit_int(),
            "UINT8": lambda decoder: decoder.decode_8bit_uint(),
            "INT16": lambda decoder: decoder.decode_16bit_int(),
            "UINT16": lambda decoder: decoder.decode_16bit_uint(),
            "INT32": lambda decoder: decoder.decode_32bit_int(),
            "UINT32": lambda decoder: decoder.decode_32bit_uint(),
            "FLOAT16": lambda decoder: decoder.decode_16bit_float(),
            "FLOAT32": lambda decoder: decoder.decode_32bit_float(),
            "INT64": lambda decoder: decoder.decode_64bit_int(),
            "UINT64": lambda decoder: decoder.decode_64bit_uint(),
            "FLOAT64": lambda decoder: decoder.decode_64bit_float(),        
        }
        return decoders[format](decoder)
    
    def _get_num_words(self, record_format: str) -> int:
        if '64' in record_format:
            num_addresses = 4
        elif '32' in record_format:
            num_addresses = 2
        else:
            num_addresses = 1
        return num_addresses
    
    def _get_server_context(self, start_address: int, count: int) -> list:
        return self.context[self.SLAVE_ID].getValues(
            fc_as_hex = self.READ_HOLDING_REGISTERS,
            address = start_address,
            count = count
        )    
    
    def _update_batch(self, start_address: int, count: int, batch: list) -> None:
        values_from_server = self._get_server_context(start_address, count)
        decoder = BinaryPayloadDecoder.fromRegisters(registers=values_from_server, byteorder=Endian.BIG)
        for register in batch:
            try:
                register.value = self._decoder_data(decoder, register.format)
            except (struct.error, ModbusException) as error:
                self._logger.error(f"{error}. Address: {register.address}, name: {register.name}")
        
    def _update_registers_from_server(self):        
        first_register = self.registers[0] 
        start_address = first_register.address
        current_address = start_address
        batch = [first_register]
        count = self._get_num_words(first_register.format)

        for register in self.registers[1:]:
            num_words = self._get_num_words(register.format)
                        
            if register.address == current_address + num_words:
                batch.append(register)
                count += num_words
            else:
                self._update_batch(start_address, count, batch)
                batch = [register]
                count = num_words
                start_address = register.address
            current_address = register.address
            
        if batch:
            self._update_batch(start_address, count, batch)
    
    def _set_server_context(self, payload: object, start_address: int) -> None:
        self.context[self.SLAVE_ID].setValues(
            fc_as_hex = self.WRITE_HOLDING_REGISTERS,
            address = start_address,
            values = payload
        )
        
    def _update_server(self, registers: list) -> None:
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG)    
        first_register = registers[0]
        start_address = first_register.address
        current_address = start_address
        self._encoder_data(builder, first_register.value, first_register.format)

        for register in registers[1:]:
            if register.address != current_address + self._get_num_words(register.format):
                self._set_server_context(builder.to_registers(), start_address)
                builder = BinaryPayloadBuilder(byteorder=Endian.BIG)
                start_address = register.address              

            self._encoder_data(builder, register.value, register.format)
            current_address = register.address

        self._set_server_context(builder.to_registers(), start_address)
    
    def _create_context(self) -> ModbusServerContext:
        storage = ModbusSlaveContext(zero_mode=True)
        context = ModbusServerContext(slaves=storage, single=True)        
        return context
    
    def _load_registers_from_bbdd(self) -> list:
        registers = self.database_manager.get_modbus_registers()
        registers_ordered_by_address = sorted(registers, key=lambda register: register.address)
        return registers_ordered_by_address
    
    def _create_index(self) -> dict:
        return { register.name: register for register in self.registers }                
        
    def update_server_from_web(self, registers: dict) -> None:
        registers_to_update = []
        
        for name, register_modified in registers.items():
            register = self.registers_index.get(name, None)
            if register:
                register.value = register_modified.get('new_value', None)
                registers_to_update.append(register)
        
        self._update_server(registers_to_update)
    
    def save_registers_from_web(self, registers: dict) -> None:
        registers_to_save = []
        
        for name, register_modified in registers.items():
            register = self.registers_index.get(name, None)
            if register: # and register_modified['value'] != register.value:
                register.value = register_modified['value']
                registers_to_save.append(register)
                             
        self.database_manager.update_registers(registers_to_save)
        
    def get_server_registers(self) -> list:
        self._update_registers_from_server()
        return self.registers
    
    def get_context(self) -> ModbusServerContext:
        return self.context   
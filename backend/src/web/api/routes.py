from flask import request, jsonify
from web.api import api
from http import HTTPStatus

def route_generator(modbus_manager) -> object:
  
    @api.route('/modbus_registers', methods=['GET','POST'])
    def modbus_registers():
        if request.method == 'POST':
            edited_registers = request.get_json()
            modbus_manager.update_server_from_web(edited_registers)     
               
            return jsonify(message='Register successfully updated'), HTTPStatus.CREATED
        else:
            registers = modbus_manager.get_server_registers()
            registers_to_json = {}
            registers_to_json['modbus_registers'] = { register.name : register.to_json() for register in registers }
        
            return registers_to_json, HTTPStatus.OK
    
    @api.route('/save_modbus_registers', methods=['POST'])
    def save_modbus_registers():
        registers = request.get_json()
        modbus_manager.save_registers_from_web(registers)
        return jsonify(message='Register successfully saved'), HTTPStatus.CREATED
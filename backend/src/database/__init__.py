import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from database.models import ModbusRegisters, Base

logger = logging.getLogger(__name__)

class DatabaseManager:
  
    SYNC_URI = 'sqlite:///./database/database.db'
  
    def __init__(self) -> None:
        engine = create_engine(self.SYNC_URI)
        Base.metadata.create_all(engine)
        self._session = sessionmaker(bind=engine)

    def get_modbus_registers(self) -> dict:
        with self._session() as session:
            try:
                modbus_registers = session.query(ModbusRegisters).all()
                return modbus_registers
            except SQLAlchemyError as error:
                logger.error(error)
    
    def update_registers(self, registers: list) -> None:
        session = self._session()
        try:
            for register in registers:                
                session.add(register)
            session.commit()
        except SQLAlchemyError as error:
            session.rollback()
            logger.error(error)
        finally:
            session.close()

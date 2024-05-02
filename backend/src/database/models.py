from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float

class Model:
  
  def to_json(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

Base = declarative_base(cls=Model)

class ModbusRegisters(Base):
  __tablename__ = 'modbus_registers'

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String, nullable=False)
  address = Column(Integer, nullable=False)
  format = Column(String, nullable=False)
  value = Column(String, nullable=False)
  scale = Column(Float)
  unit = Column(String)
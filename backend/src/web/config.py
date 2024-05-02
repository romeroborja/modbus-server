from os import environ

class Config():
  ENV = environ.get('ENV')
  DEBUG = False
  IP = "0.0.0.0"
  PORT = 5000
  SECRET_KEY = "b0f81124dc257b86a00a2768a60c4391d64e1ce2b99ddfdca86ccc226fbc51a1"
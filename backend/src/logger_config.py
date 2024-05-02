from logging.config import dictConfig
import logging

logger_config = {
  'version': 1,
  'disable_existing_loggers': False,
  'handlers': {
    'console_handler': {
      'class': 'logging.StreamHandler',
      'formatter': 'default_formatter',
    },
  },
  'formatters': {
    'default_formatter': {
      'format': '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    }
  },
  'loggers': {
    '': {
      'handlers': ['console_handler'],
      'level': logging.DEBUG,
    }
  },
}

dictConfig(logger_config)
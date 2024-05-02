import gunicorn.app.base
import logging

from gunicorn import glogging

class CustomGunicornLogger(glogging.Logger):
    def setup(self, cfg):
        super().setup(cfg)
        formatter = logging.Formatter('%(asctime)s | gunicorn | %(levelname)s | %(message)s')
        for handler in self.error_log.handlers:
            handler.setFormatter(formatter)
            handler.setLevel(logging.DEBUG)
        for handler in self.access_log.handlers:
            handler.setFormatter(formatter)
            handler.setLevel(logging.DEBUG)
        
logger_class = CustomGunicornLogger

def get_config(host, port):
    options = {
        'bind': '%s:%s' % (host, port),
        'workers': 1,
        'threads': 1,
        'logger_class': logger_class,
    }

    return options

class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
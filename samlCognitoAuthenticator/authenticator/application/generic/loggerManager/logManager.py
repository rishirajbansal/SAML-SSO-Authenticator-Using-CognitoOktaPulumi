import os


class LogManager:

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(asctime)s [pid:%(process)d tid:%(thread)d] [%(module)s:%(lineno)s - %(funcName)s()] [%('
                          'levelname)s] :- %(message)s '
            },
            'simple': {
                'format': '%(levelname)s %(asctime)s %(module)s :- %(message)s'
            },
        },
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            'log_file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(os.getenv("LOG_LOC"), 'logs/authenticator.log'),
                'maxBytes': 5120,  # 5 MB
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'log_file'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['console', 'log_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'application': {
                'handlers': ['console', 'log_file'],
                'level': 'DEBUG',
                'propagate': False,
            }
        }
    }

    def __init__(self):
        pass

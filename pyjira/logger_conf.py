from pyjira.databases import app_settings

log_level = "DEBUG" if app_settings.debug_mode else app_settings.log_level

log_config = dict(
    version=1,
    disable_existing_loggers=app_settings.disable_existing_loggers,
    formatters={
        "default": {
            "format": app_settings.log_format,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    handlers={
        "default": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "default",
        }
    },
    loggers={
        app_settings.logger_name: {
            "handlers": ["default"],
            "propagate": False,
            "level": log_level,
        }
    },
)

import logging

formatter = logging.Formatter(
    fmt="%(levelname)s - %(asctime)s - pytwilio - %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_logger(name: str) -> logging.Logger:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    return logger


def set_uvicorn_loggers() -> None:
    uvicorn_handler = logging.StreamHandler()
    uvicorn_handler.setLevel(logging.INFO)
    uvicorn_handler.setFormatter(formatter)

    logger_uvicorn_access = logging.getLogger("uvicorn.access")
    logger_uvicorn_access.handlers.clear()
    logger_uvicorn_access.addHandler(uvicorn_handler)

    logger_uvicorn_error = logging.getLogger("uvicorn.error")
    # Prevents dupplicate logging from uvicorn
    logger_uvicorn_error.propagate = False
    logger_uvicorn_error.addHandler(uvicorn_handler)

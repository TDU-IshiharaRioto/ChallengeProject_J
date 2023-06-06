from .ExceptionMessage import ExceptionMessage

class TimeServerNotFoundException(Exception):
    def __init__(self):
        super().__init__(ExceptionMessage.getWeatherServerNotFoundExceptionMessage())
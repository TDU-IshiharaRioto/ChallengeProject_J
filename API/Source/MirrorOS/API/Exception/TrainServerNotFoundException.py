from .ExceptionMessage import ExceptionMessage

class TrainServerNotFoundException(Exception):
    def __init__(self):
        super().__init__(ExceptionMessage.getTrainServerNotFoundExceptionMessage())

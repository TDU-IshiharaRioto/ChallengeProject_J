# エラーメッセージをまとめたクラス

class ExceptionMessage:
    @staticmethod
    def getTimeServerNotFoundExceptionMessage():
        return "エラー：タイムサーバがみつかりませんでした。"
    
    def getWeatherServerNotFoundExceptionMessage():
        return "エラー：天気サーバがみつかりませんでした。"
    
    def getTrainServerNotFoundExceptionMessage():
        return "エラー：交通状況サーバが見つかりませんでした。"
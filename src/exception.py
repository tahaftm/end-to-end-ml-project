import sys
from src.logger import logging

def error_message_detail(error, error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    error_msg = f"Error occured in \n python script: {exc_tb.tb_frame.f_code.co_filename} \n line number: {exc_tb.tb_lineno} \n error message: {str(error)}"
    return error_msg

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message,error_detail=error_detail)

    def __str__(self):
        return self.error_message
    
if __name__ == "__main__":
    try:
        a = 1/0
    except Exception as e:
        logging.info("Diviion by zero")
        raise CustomException(e,sys)
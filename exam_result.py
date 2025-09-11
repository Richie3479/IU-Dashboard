import datetime

class ExamResult:
    def __init__(self, mark:float, date:datetime, passed:bool):
        self._mark = mark
        self._date = date
        self._passed = passed

    def get_mark(self):
        return self._mark
    
    def set_mark(self, mark):
        self._mark = mark
    
    def get_date(self):
        return self._date
    
    def set_date(self, date):
        self._date = date
    
    def get_passed(self):
        return self._passed
    
    def set_passed(self, passed):
        self._passed = passed
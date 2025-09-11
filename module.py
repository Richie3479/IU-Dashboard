import datetime
import math

from exam_result import ExamResult

class Module:
    def __init__(self, name:str, ects:int, status:str, mark:float = None, date:datetime = None, passed:bool = None):
        self._name = name
        self._ects = ects
        self._status = status
        self._performance = None

        self.create_or_update_performance(mark, date, passed)

    def get_name(self):
        return self._name
    
    def get_ects(self):
        return self._ects
    
    def get_status(self):
        return self._status
    
    def get_performance(self):
        return self._performance
    
    def set_new_status(self, new_status):
        self._status = new_status
    
    def create_or_update_performance(self, mark, date, passed):
        if self.is_value_valid(mark) and self.is_value_valid(date) and self.is_value_valid(passed):
            if self.get_performance():
                # --- Update bestehendes Objekt ---
                self._performance.set_mark(mark)
                self._performance.set_date(date)
                self._performance.set_passed(passed)
            else:
                # --- Neues Objekt erstellen ---
                self._performance = ExamResult(mark, date, passed)
        else:
            # --- Ungültige Daten: Leistung löschen ---
            self._performance = None
    
    # --- Ein Wert ist gültig, wenn er nicht None, kein NaN und kein leerer String ist ---
    def is_value_valid(self, value):    
        if value is None:   
            return False
        if isinstance(value, float) and math.isnan(value):
            return False
        if isinstance(value, str) and value.strip() == "":
            return False
        return True
    
    # --- Wandelt das Objekt inkl. Prüfungsleistung (wenn vorhanden) in ein Dictionary um ---
    def to_dict(self):  
        performance = self.get_performance()
        return {
            "Name": self.get_name(),
            "ECTS": self.get_ects(),
            "Status": self.get_status(),
            "Note": performance.get_mark() if performance else "",
            "Datum": performance.get_date().strftime("%d.%m.%Y") if performance else "",
            "Bestanden": "Ja" if performance and performance.get_passed() else ("Nein" if performance else "")
        }
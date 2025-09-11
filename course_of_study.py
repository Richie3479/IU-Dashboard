from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from semester import Semester

class CourseOfStudy:
    def __init__(self, name:str, type:str, titel:str, total_ects:int, duration:str, start:datetime, end:datetime, designation:list):
        self._name = name
        self._type = type
        self._titel = titel
        self._total_ects = total_ects
        self._duration = duration
        self._start = start
        self._end = end

        self._semester = [Semester(d) for d in designation]

    def get_total_ects(self):
        return self._total_ects
    
    def get_end(self):
        return self._end
    
    def get_semester(self):
        return self._semester

    # --- Berechnet die Zeit von jetzt bis zum angegebenen Ende ---
    def get_time_left(self):
        time_left = relativedelta(self.get_end(), datetime.now())
        return time_left
    
    # --- Berechnet die bis dato erreichten ECTS-Punkte ---
    def calculate_reached_ects(self):
        reached_ects = 0

        for semester in self.get_semester():
            for module in semester.get_modules():
                performance = module.get_performance()
                if performance is not None and performance.get_passed():
                    reached_ects += module.get_ects()

        return reached_ects
    
    # --- Berechnet den gesamtfortschritt in % ---
    def get_ects_progress(self):
        progress = (self.calculate_reached_ects()/self.get_total_ects())*100
        return round(progress, 2) 

    # --- Berechnet wie viel ECTS-Punkte pro Monat notwendig sind um bis zum angegebenen Ende mit dem Studium fertig zu werden ---
    def get_necessary_ects_pm(self):
        missing_ects = self.get_total_ects() - self.calculate_reached_ects()
        time_left = self.get_time_left()
        total_months = time_left.years * 12 + time_left.months

        # --- Wenn noch Tage übrig sind, als "fast ein Monat" zählen ---
        if time_left.days > 0:
            total_months += 1

        if total_months <= 0:
            return float('inf')

        ects_pm = missing_ects / total_months
        return round(ects_pm, 2)
    
    # --- Berechnet wie viel ects diesen Monat erreicht wurden ---
    def get_ects_this_month(self):
        reached_ects_this_month = 0
        time_now = datetime.now()

        for semester in self.get_semester():
            for module in semester.get_modules():
                performance = module.get_performance()
                if performance is not None and performance.get_passed():
                    performance_date = performance.get_date()
                    if (performance_date.year == time_now.year and performance_date.month == time_now.month):
                        reached_ects_this_month += module.get_ects()
        
        return reached_ects_this_month
    
    # --- Gibt alle erreichten Noten zurück ---
    def get_grades_achieved(self):
        grades = [
            module.get_performance().get_mark()
            for semester in self.get_semester()
            for module in semester.get_modules()
            if module.get_performance() is not None and module.get_performance().get_passed()
        ]

        if grades:
            return grades
        else:
            return 0

    # --- Berechnet den Notendurchschnitt ---
    def calculate_gpa(self):
        grades = self.get_grades_achieved()
        if grades == 0:
            return 0

        return round(sum(grades) / len(grades), 1)

    # --- Gibt die beste und schlechteste Note zurück die erreicht wurde ---
    def get_best_worst_mark(self):
        grades = self.get_grades_achieved()

        if grades == 0:     # --- Wenn noch keine Note existiert ---
            grades = None
            return "Keine", "Keine"

        best_mark = min(grades)
        worst_mark = max(grades)

        return round(best_mark, 1), round(worst_mark, 1)

    # --- Berechnet die notwendige Note um auf einen durchschnitt von 2.0 zu kommen ---
    def calculate_required_next_mark(self):
        target_average = 2.0
        grades = self.get_grades_achieved()

        if grades == 0:     # --- Wenn noch keine Note existiert ---
            return target_average   
        else:
            count_grades = len(grades) 

        summe = sum(grades)
        needed_mark = target_average * (count_grades + 1) - summe

        return round(needed_mark, 1)
    
    def update_module_performance(self, module_name, mark, date):
        for semester in self.get_semester():
            for module in semester.get_modules():
                if module.get_name() == module_name:
                    passed = mark <= 4.0
                    module.create_or_update_performance(mark, date, passed)
                    if passed:
                        module.set_new_status("Abgeschlossen")

    # --- Speichert alle Modul-Dictionaries in modules_data und schreibt sie in eine neue CSV-Datei ---
    def save_modules_csv(self, module_csv_path: str):
        try:
            modules_data = []
            for semester in self.get_semester():
                for module in semester.get_modules():
                    modules_data.append(module.to_dict())
            df = pd.DataFrame(modules_data)
            df.to_csv(module_csv_path, index=False)
        except(IOError, OSError) as e:
            print(f"Fehler beim Schreiben der Datei '{module_csv_path}': {e}")
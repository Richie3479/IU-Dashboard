from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from semester import Semester

class CourseOfStudy:
    """
    Repräsentiert einen vollständigen Studienverlauf.

    Enthält Informationen wie Name, Abschluss, Studiendauer, ECTS-Ziel sowie
    eine Liste von Semestern mit zugehörigen Modulen.
    """
    def __init__(self, name:str, type:str, titel:str, total_ects:int, duration:str, start:datetime, end:datetime, designation:list):
        """
        Initialisiert ein neues CourseOfStudy-Objekt.

        Args:
            name (str): Studiengangsname.
            type (str): Studienart (z.B. Bachelor, Master).
            titel (str): Verliehener Titel (z.B. B.Sc.).
            total_ects (int): Gesamtanzahl der zu erreichenden ECTS-Punkte.
            duration (str): Gesamtdauer des Studiums.
            start (datetime): Startdatum des Studiums.
            end (datetime): Voraussichtliches Enddatum des Studiums.
            designation (list): Liste von Semesterbezeichnungen.
        """
        self._name = name
        self._type = type
        self._titel = titel
        self._total_ects = total_ects
        self._duration = duration
        self._start = start
        self._end = end

        self._semester = [Semester(d) for d in designation]

    def get_total_ects(self):
        """
        Gibt die Gesamtanzahl der im Studium vorgesehenen ECTS zurück.

        Returns:
            int: Gesamt-ECTS.
        """
        return self._total_ects
    
    def get_end(self):
        """
        Gibt das geplante Enddatum des Studiums zurück.

        Returns:
            datetime: Enddatum.
        """
        return self._end
    
    def get_semester(self):
        """
        Gibt die Liste aller Semester im Studienverlauf zurück.

        Returns:
            list: Liste von Semester-Objekten.
        """
        return self._semester

    def get_time_left(self):
        """
        Berechnet die verbleibende Zeit bis zum Studienende.

        Returns:
            relativedelta: Zeitdifferenz zwischen jetzt und dem Enddatum.
        """
        time_left = relativedelta(self.get_end(), datetime.now())
        return time_left
    
    def calculate_reached_ects(self):
        """
        Berechnet die Anzahl der bereits erreichten ECTS-Punkte.

        Returns:
            int: Erreichte ECTS.
        """
        reached_ects = 0

        for semester in self.get_semester():
            for module in semester.get_modules():
                performance = module.get_performance()
                if performance is not None and performance.get_passed():
                    reached_ects += module.get_ects()

        return reached_ects
    
    def get_ects_progress(self):
        """
        Berechnet den Fortschritt des Studiums in Prozent.

        Returns:
            float: Prozentualer Fortschritt, gerundet auf 2 Stellen.
        """
        progress = (self.calculate_reached_ects()/self.get_total_ects())*100
        return round(progress, 2) 

    def get_necessary_ects_pm(self):
        """
        Berechnet, wie viele ECTS-Punkte pro Monat erforderlich sind,
        um das Studium bis zum geplanten Enddatum abzuschließen.

        Returns:
            float: Benötigte ECTS pro Monat, gerundet auf 2 Stellen.
        """
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
    
    def get_ects_this_month(self):
        """
        Berechnet, wie viele ECTS-Punkte im aktuellen Monat erreicht wurden.

        Returns:
            int: ECTS-Punkte im aktuellen Monat.
        """
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
    
    def get_grades_achieved(self):
        """
        Gibt alle erreichten Noten (bestandene Prüfungen) zurück.

        Returns:
            list or int: Liste von Noten oder 0, wenn keine vorhanden sind.
        """
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

    def calculate_gpa(self):
        """
        Berechnet den aktuellen Notendurchschnitt (GPA).

        Returns:
            float: Durchschnittsnote, gerundet auf eine Nachkommastelle.
        """
        grades = self.get_grades_achieved()
        if grades == 0:
            return 0

        return round(sum(grades) / len(grades), 1)

    def get_best_worst_mark(self):
        """
        Gibt die beste und schlechteste erzielte Note zurück.

        Returns:
            tuple: (Beste Note, Schlechteste Note) oder ("Keine", "Keine"), wenn keine vorhanden sind.
        """
        grades = self.get_grades_achieved()

        if grades == 0:     # --- Wenn noch keine Note existiert ---
            grades = None
            return "Keine", "Keine"

        best_mark = min(grades)
        worst_mark = max(grades)

        return round(best_mark, 1), round(worst_mark, 1)

    def calculate_required_next_mark(self):
        """
        Berechnet die benötigte nächste Note, um einen Durchschnitt von 2.0 zu erreichen.

        Returns:
            float: Benötigte Note.
        """

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
        """
        Aktualisiert die Prüfungsleistung eines Moduls anhand des Namens.

        Args:
            module_name (str): Name des Moduls.
            mark (float): Neue Note.
            date (datetime): Datum der bestandenen Prüfung.
        """
        for semester in self.get_semester():
            for module in semester.get_modules():
                if module.get_name() == module_name:
                    passed = mark <= 4.0
                    module.create_or_update_performance(mark, date, passed)
                    if passed:
                        module.set_new_status("Abgeschlossen")

    def save_modules_csv(self, module_csv_path: str):
        """
        Speichert alle Modul-Informationen als CSV-Datei.

        Args:
            module_csv_path (str): Pfad zur Ausgabedatei.
        """
        try:
            modules_data = []
            for semester in self.get_semester():
                for module in semester.get_modules():
                    modules_data.append(module.to_dict())
            df = pd.DataFrame(modules_data)
            df.to_csv(module_csv_path, index=False)
        except(IOError, OSError) as e:
            print(f"Fehler beim Schreiben der Datei '{module_csv_path}': {e}")
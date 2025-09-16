import datetime
import math

from exam_result import ExamResult

class Module:
    """
    Repräsentiert ein Studienmodul mit zugehöriger Prüfungsleistung.

    Ein Modul besteht aus einem Namen, ECTS-Punkten, einem Status und optional einer Prüfungsleistung,
    die als ExamResult-Objekt gespeichert wird.
    """
    def __init__(self, name:str, ects:int, status:str, mark:float = None, date:datetime = None, passed:bool = None):
        """
        Initialisiert ein neues Modul-Objekt mit den angegebenen Informationen.

        Args:
            name (str): Name des Moduls.
            ects (int): Anzahl der ECTS-Punkte.
            status (str): Aktueller Status des Moduls (z. B. "belegt", "abgeschlossen").
            mark (float, optional): Note der Prüfungsleistung.
            date (datetime.datetime, optional): Datum der Prüfung.
            passed (bool, optional): True, wenn die Prüfung bestanden wurde, sonst False.
        """
        self._name = name
        self._ects = ects
        self._status = status
        self._performance = None

        self.create_or_update_performance(mark, date, passed)

    def get_name(self):
        """
        Gibt den Namen des Moduls zurück.

        Returns:
            str: Modulname.
        """
        return self._name
    
    def get_ects(self):
        """
        Gibt die Anzahl der ECTS-Punkte des Moduls zurück.

        Returns:
            int: ECTS-Punkte.
        """
        return self._ects
    
    def get_status(self):
        """
        Gibt den aktuellen Status des Moduls zurück.

        Returns:
            str: Modulstatus.
        """
        return self._status
    
    def get_performance(self):
        """
        Gibt das ExamResult-Objekt (Prüfungsleistung) zurück, falls vorhanden.

        Returns:
            ExamResult or None: Prüfungsleistung oder None, wenn keine vorhanden ist.
        """
        return self._performance
    
    def set_new_status(self, new_status):
        """
        Setzt einen neuen Status für das Modul.

        Args:
            new_status (str): Neuer Status (z. B. "abgeschlossen").
        """
        self._status = new_status
    
    def create_or_update_performance(self, mark, date, passed):
        """
        Erstellt oder aktualisiert die Prüfungsleistung (ExamResult) des Moduls,
        sofern gültige Werte übergeben wurden. Bei ungültigen Werten wird die Leistung entfernt.

        Args:
            mark (float): Note.
            date (datetime.datetime): Prüfungsdatum.
            passed (bool): True bei bestanden, sonst False.
        """
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
    
    def is_value_valid(self, value):  
        """
        Prüft, ob ein übergebener Wert gültig ist.

        Ein Wert ist gültig, wenn er:
        - nicht None ist,
        - kein NaN (Not a Number) ist (bei float),
        - kein leerer String ist (bei str).

        Args:
            value: Zu prüfender Wert.

        Returns:
            bool: True, wenn der Wert gültig ist, sonst False.
        """  
        if value is None:   
            return False
        if isinstance(value, float) and math.isnan(value):
            return False
        if isinstance(value, str) and value.strip() == "":
            return False
        return True
    
    def to_dict(self):  
        """
        Wandelt das Modul-Objekt inklusive Prüfungsleistung (falls vorhanden)
        in ein Dictionary um, geeignet zur Anzeige oder Weiterverarbeitung.

        Returns:
            dict: Wörterbuch mit den Modul-Informationen.
        """
        performance = self.get_performance()
        return {
            "Name": self.get_name(),
            "ECTS": self.get_ects(),
            "Status": self.get_status(),
            "Note": performance.get_mark() if performance else "",
            "Datum": performance.get_date().strftime("%d.%m.%Y") if performance else "",
            "Bestanden": "Ja" if performance and performance.get_passed() else ("Nein" if performance else "")
        }
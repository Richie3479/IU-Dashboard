import datetime

class ExamResult:
    """
    Repräsentiert das Ergebnis einer Prüfungsleistung in einem Modul.

    Enthält Informationen über die Note, das Prüfungsdatum und den Status (bestanden/nicht bestanden).
    """
    def __init__(self, mark:float, date:datetime, passed:bool):
        """
        Initialisiert ein neues ExamResult-Objekt.

        Args:
            mark (float): Die erzielte Note.
            date (datetime.datetime): Das Datum der Prüfung.
            passed (bool): True, wenn die Prüfung bestanden wurde, sonst False.
        """
        self._mark = mark
        self._date = date
        self._passed = passed

    def get_mark(self):
        """
        Gibt die erzielte Note zurück.

        Returns:
            float: Die Note.
        """
        return self._mark
    
    def set_mark(self, mark):
        """
        Legt die Note fest.

        Args:
            mark (float): Die neue Note.
        """
        self._mark = mark
    
    def get_date(self):
        """
        Gibt das Datum der Prüfung zurück.

        Returns:
            datetime.datetime: Das Prüfungsdatum.
        """
        return self._date
    
    def set_date(self, date):
        """
        Legt das Datum der Prüfung fest.

        Args:
            date (datetime.datetime): Das neue Datum.
        """
        self._date = date
    
    def get_passed(self):
        """
        Gibt zurück, ob die Prüfung bestanden wurde.

        Returns:
            bool: True bei bestanden, False sonst.
        """
        return self._passed
    
    def set_passed(self, passed):
        """
        Legt fest, ob die Prüfung bestanden wurde.

        Args:
            passed (bool): True bei bestanden, False sonst.
        """
        self._passed = passed
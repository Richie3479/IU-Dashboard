class Semester:
    """
    Repräsentiert ein Semester innerhalb eines Studienverlaufs.

    Ein Semester enthält eine Bezeichnung (z.B. "1. Semester") und eine Liste von Modulen,
    die diesem Semester zugeordnet sind.
    """
    def __init__(self, designation:str):
        """
        Initialisiert ein neues Semester-Objekt mit der gegebenen Bezeichnung.

        Args:
            designation (str): Bezeichnung des Semesters (z.B. "Semester 1").
        """
        self._designation = designation
        self._modules = []

    def add_module(self, module):
        """
        Fügt dem Semester ein Modul hinzu.

        Args:
            module (Module): Das hinzuzufügende Modul.

        Returns:
            None
        """
        return self._modules.append(module)
    
    def get_designation(self):
        """
        Gibt die Bezeichnung des Semesters zurück.

        Returns:
            str: Semesterbezeichnung.
        """
        return self._designation
    
    def get_modules(self):
        """
        Gibt die Liste der dem Semester zugeordneten Module zurück.

        Returns:
            list: Liste der Module.
        """
        return self._modules
    
    def get_progress(self):
        """
        Ermittelt den Fortschritt des Semesters anhand der Modul-Status.

        Zählt die Anzahl der offenen und abgeschlossenen Module.

        Returns:
            tuple: (Anzahl offene Module, Anzahl abgeschlossene Module)
        """
        open_modules = 0
        finished_modules = 0

        for module in self.get_modules():
            if module.get_status() == "Abgeschlossen":
                finished_modules += 1
            elif module.get_status() == "Offen":
                open_modules += 1

        return open_modules, finished_modules
    

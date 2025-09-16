class Controller:
    """
    Steuert den Zugriff auf ein CourseOfStudy-Objekt und stellt zentrale Funktionen bereit.

    Diese Klasse dient als Schnittstelle zwischen der Anwendungslogik und der GUI
    """
    def __init__(self, course_of_study):
        """
        Initialisiert den Controller mit einem gegebenen Studienverlauf.

        Args:
            course_of_study (CourseOfStudy): Ein Objekt des Studienverlaufs.
        """
        self._course = course_of_study
        
    def get_course(self):
        """
        Gibt das zugehörige CourseOfStudy-Objekt zurück.

        Returns:
            CourseOfStudy: Studienverlauf.
        """
        return self._course
    
    def update_performance(self, module_name, mark, date):
        """
        Aktualisiert die Prüfungsleistung eines bestimmten Moduls und speichert alle Module in einer CSV-Datei.

        Args:
            module_name (str): Name des Moduls.
            mark (float): Neue Note.
            date (datetime): Datum der Prüfung.
        """
        self.get_course().update_module_performance(module_name, mark, date)
        self.get_course().save_modules_csv("modules.csv")

    def get_semester_progress(self, semester_number):
        """
        Gibt den Fortschritt (offene/abgeschlossene Module) eines bestimmten Semesters zurück.

        Args:
            semester_number (int): Index des Semesters (beginnend bei 0).

        Returns:
            tuple: (Anzahl offene Module, Anzahl abgeschlossene Module)
        """
        return self.get_course().get_semester()[semester_number].get_progress()
    
    def get_semester_designation(self, semester_number):
        """
        Gibt die Bezeichnung eines bestimmten Semesters zurück.

        Args:
            semester_number (int): Index des Semesters.

        Returns:
            str: Semesterbezeichnung.
        """
        return self.get_course().get_semester()[semester_number].get_designation()
    
    def get_all_open_modules(self):
        """
        Gibt eine Liste aller offenen Module im Studienverlauf zurück.

        Returns:
            list: Liste von Modulnamen mit Status "Offen".
        """
        all_modules = []
        for semester in self.get_course().get_semester():
            for module in semester.get_modules():
                if module.get_status() == "Offen":
                    all_modules.append(module.get_name())
        return all_modules
    
    def time_left_display(self):
        """
        Gibt die verbleibende Zeit bis zum Studienende als formatierten Text zurück.

        Beispiel: "1 Jahr 3 Monate 12 Tage"

        Returns:
            str: Formatierte Zeitangabe.
        """
        time_left = self.get_course().get_time_left()

        def pluralize(value, singular, plural):
            if value == 1:
                return singular
            elif value > 1:
                return plural
            else:
                return ""

        year_str = f"{time_left.years} {pluralize(time_left.years, 'Jahr', 'Jahre')}" if time_left.years > 0 else ""
        month_str = f"{time_left.months} {pluralize(time_left.months, 'Monat', 'Monate')}" if time_left.months > 0 else ""
        day_str = f"{time_left.days} {pluralize(time_left.days, 'Tag', 'Tage')}" if time_left.days > 0 else ""

        parts = [part for part in [year_str, month_str, day_str] if part]
        return " ".join(parts)
    
    def next_mark_setting(self):
        """
        Gibt an, welche Note als nächstes erforderlich ist, um einen Durchschnitt von 2.0 zu erreichen.

        Rückgabewerte:
        - Zahl: Erforderliche Note (z.B. 1.7)
        - "Egal": Durchschnitt bereits unter 2.0.
        - "Nicht möglich": Durchschnitt ist nicht mehr erreichbar.

        Returns:
            float or str: Nächste notwendige Note.
        """
        next_mark = self.get_course().calculate_required_next_mark() 
        if next_mark > 6:
            next_mark = "Egal"
        elif next_mark < 1:
            next_mark = "Nicht möglich"
        else:
            next_mark
        return next_mark

    def get_metrics(self):
        """
        Gibt eine Zusammenfassung wichtiger Leistungskennzahlen des Studienverlaufs zurück.

        Returns:
            dict: Übersicht mit Metriken (ECTS, Noten, Fortschritt, Zeit usw.).
        """
        return {
            "reached_ects": self.get_course().calculate_reached_ects(),
            "total_ects": self.get_course().get_total_ects(),
            "progress_percent": self.get_course().get_ects_progress(),
            "gpa": self.get_course().calculate_gpa(),
            "best_mark": self.get_course().get_best_worst_mark()[0],
            "worst_mark": self.get_course().get_best_worst_mark()[1],
            "time_left": self.get_course().get_time_left(),
            "semester": self.get_course().get_semester(),
            "ects_this_month": self.get_course().get_ects_this_month(),
            "necessary_ects_pm": self.get_course().get_necessary_ects_pm()
        }
class Controller:
    def __init__(self, course_of_study):
        self._course = course_of_study
        
    def get_course(self):
        return self._course
    
    def update_performance(self, module_name, mark, date):
        self.get_course().update_module_performance(module_name, mark, date)
        self.get_course().save_modules_csv("modules.csv")

    def get_semester_progress(self, semester_number):
        return self.get_course().get_semester()[semester_number].get_progress()
    
    def get_semester_designation(self, semester_number):
        return self.get_course().get_semester()[semester_number].get_designation()
    
    def get_all_open_modules(self):
        all_modules = []
        for semester in self.get_course().get_semester():
            for module in semester.get_modules():
                if module.get_status() == "Offen":
                    all_modules.append(module.get_name())
        return all_modules
    
    def time_left_display(self):
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
        next_mark = self.get_course().calculate_required_next_mark() 
        if next_mark > 6:
            next_mark = "Egal"
        elif next_mark < 1:
            next_mark = "Nicht möglich"
        else:
            next_mark
        return next_mark

    def get_metrics(self):
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
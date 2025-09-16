import tkinter as tk
import pandas as pd
import tkinter.messagebox as mb

from gui import Gui
from course_of_study import CourseOfStudy
from module import Module
from controller import Controller

def main():
    """
    Hauptfunktion zum Laden der CSV-Daten, Erstellen der Objekte und Starten der GUI.

    Lädt Studiengang-, Semester- und Moduldaten aus CSV-Dateien,
    wandelt Datenformate um, erstellt Objekte für Studiengang, Semester und Module,
    initialisiert den Controller und startet die grafische Benutzeroberfläche.
    """
    try:
        course_of_study_df = pd.read_csv("course_of_study.csv")
        semester_df = pd.read_csv("semester.csv")
        modules_df = pd.read_csv("modules.csv")
    except FileNotFoundError:
        mb.showerror("Eine Datei wurde nicht gefunden.")
    except pd.errors.EmptyDataError:
        mb.showerror("Eine Datei ist leer oder ungültig.")
    except Exception as e:
        mb.showerror(f"Fehler beim Laden der CSV: {e}")


    # --- Objekte erstellen ---
    # --- Datentypen korrigieren ---
    course_of_study_df["Start"] = pd.to_datetime(course_of_study_df["Start"], errors="coerce", dayfirst=True)
    course_of_study_df["Ende"] = pd.to_datetime(course_of_study_df["Ende"], errors="coerce", dayfirst=True)

    modules_df["Note"] = pd.to_numeric(modules_df["Note"], errors="coerce")
    modules_df["Datum"] = pd.to_datetime(modules_df["Datum"], errors="coerce", dayfirst=True)
    modules_df["Bestanden"] = modules_df["Bestanden"].map({"Ja": True, "Nein": False})

    # --- Studiengang und Semester erstellen ---
    semester_list = semester_df["Bezeichnung"].tolist()

    for row in course_of_study_df.itertuples():
        my_course_of_study = CourseOfStudy(
            row.Name,
            row.Art,
            row.Titel,
            row.Gesamt_ECTS,
            row.Dauer,
            row.Start,
            row.Ende,
            semester_list
        )

    # --- Module erstellen ---
    all_modules = []

    for row in modules_df.itertuples():
        module = Module(
            row.Name, 
            row.ECTS, 
            row.Status, 
            row.Note, 
            row.Datum, 
            row.Bestanden
        )
        all_modules.append(module)

    # --- Semester erstellen ---
    module_indices_per_semester = [
        range(0, 6),   # Semester 1
        range(6, 12),  # Semester 2
        range(12, 18), # Semester 3
        range(18, 24), # Semester 4
        range(24, 30), # Semester 5
        range(30, 33)  # Semester 6
    ]

    for semester_index, module_range in enumerate(module_indices_per_semester):
        for module_index in module_range:
            my_course_of_study.get_semester()[semester_index].add_module(all_modules[module_index])

    controller = Controller(my_course_of_study)
    # --- Tkinter Setup & Dashboard starten ---
    root = tk.Tk()
    app = Gui(root, my_course_of_study, controller)
    app.run()

if __name__ == "__main__":
    main()
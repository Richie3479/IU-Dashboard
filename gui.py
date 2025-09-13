from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox as mb

class Gui:
    def __init__(self, root, course_of_study, controller):
        self._root = root
        self._course_of_study = course_of_study
        self.controller = controller

        # --- Bildschirmgröße holen ---
        self.screen_width = self.get_root().winfo_screenwidth()
        self.screen_height = self.get_root().winfo_screenheight()

        # --- Anpassung von tkinter ---
        self.tk_settings()

        # --- Progressbar ---
        self.create_progressbar()
        
        # --- Tabelle 1 ---
        self.create_table1()
       
        # --- Tabelle 2 ---
        self.create_table2()
        
        # --- Tabelle für Semester 1 - 3 ---
        self.create_table3()

        # --- Tabelle für Semester 4 - 6 ---
        self.create_table4()

        # --- Hinzufügen Knopf ---
        self.add_performance_button = tk.Button(self._root, text="Hinzufügen", command=self.add_performance)
        self.add_performance_button.pack()

        # --- Sicheres Schließen ---
        self._root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def get_root(self):
        return self._root
    
    def get_screen_width(self):
        return self.screen_width
    
    def get_screen_height(self):
        return self.screen_height
    
    # --- Einstellungen für das tkinter Fenster ---
    def tk_settings(self):
        self.get_root().title("Dashboard")
        self.get_root().geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.get_root().state("zoomed")
        self.get_root().configure(bg="Gray")
    
    # --- Erstellung der Progressbar
    def create_progressbar(self):
        # --- Einstellungen der Progressbar ---
        self.progress_bar = ttk.Progressbar(
            self.get_root(), 
            orient="horizontal", 
            length=self.get_screen_width() * 0.9, 
            mode="determinate", 
            value= self.controller.get_metrics()["reached_ects"], 
            maximum= self.controller.get_metrics()["total_ects"]
        )
        self.progress_bar.pack(pady=20)

        # --- Einstellungen für die %-Anzeige der Progressbar ---
        self.progress_label = tk.Label(
            self.get_root(), 
            text=(f"{self.controller.get_metrics()["progress_percent"]}%"), 
            font=("Arial", 10, "bold")
        )
        self.progress_label.place(in_=self.progress_bar, relx=0.5, rely=0.5, anchor="center")

    # --- Vordefinierte Header Einstellung ---
    def table_header_config(self, headers, table_frame):
        for col, text in enumerate(headers):
            label = tk.Label(table_frame, text=text, bg="#2C5C8C", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
            label.grid(row=0, column=col, sticky="nsew")

    # --- Vordefinierte Text Einstellung ---
    def table_values_config(self, values, table_frame):
        for col, text in enumerate(values):
            label = tk.Label(table_frame, text=text, font=("Arial", 11), padx=10, pady=5)
            label.grid(row=1, column=col, sticky="nsew")

    # --- Tabelle 1 erstellen ---
    def create_table1(self):
        if hasattr(self, 'table1_frame'):
            self.table1_frame.destroy()
        self.table1_frame = tk.Frame(self._root)
        self.table1_frame.pack(pady=20)

        headers = [
            "Verbleibende Zeit", 
            "Erreichte ECTS", 
            "Notwendige ECTS pro Monat", 
            "Diesen Monat erreichte ECTS"
        ]

        self.table_header_config(headers, self.table1_frame)

        values = [
            self.controller.time_left_display(),
            f"{self.controller.get_metrics()["reached_ects"]}/{self.controller.get_metrics()["total_ects"]}",
            self.controller.get_metrics()["necessary_ects_pm"],
            self.controller.get_metrics()["ects_this_month"]
        ]
        
        self.table_values_config(values, self.table1_frame)

    # --- Tabelle 2 erstellen ---
    def create_table2(self):
        if hasattr(self, 'table2_frame'):
            self.table2_frame.destroy()   
        self.table2_frame = tk.Frame(self._root)
        self.table2_frame.pack(pady=20)

        headers = [
            "Aktueller Notendurchschnitt", 
            "Beste Note", 
            "Schlechteste Note", 
            "Nächste Note muss besser sein als:"
        ]

        self.table_header_config(headers, self.table2_frame)
        
        values = [
            self.controller.get_metrics()["gpa"],
            self.controller.get_metrics()["best_mark"],
            self.controller.get_metrics()["worst_mark"],
            self.controller.next_mark_setting()
        ]

        self.table_values_config(values, self.table2_frame)

    # --- Tabelle 3 für die Semester erstellen ---
    def create_table3(self):
        if hasattr(self, 'table3_frame'):
            self.table3_frame.destroy() 
        self.table3_frame = tk.Frame(self._root)
        self.table3_frame.pack(pady=20, fill=tk.BOTH)

        canvas1 = self.pie_diagram(1, self.table3_frame)
        canvas2 = self.pie_diagram(2, self.table3_frame)
        canvas3 = self.pie_diagram(3, self.table3_frame)

        canvas1.get_tk_widget().pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        canvas2.get_tk_widget().pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        canvas3.get_tk_widget().pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    # --- Tabelle 4 für die Semester erstellen ---
    def create_table4(self):
        if hasattr(self, 'table4_frame'):
            self.table4_frame.destroy()
        self.table4_frame = tk.Frame(self._root)
        self.table4_frame.pack(pady=20, fill=tk.BOTH)

        canvas1 = self.pie_diagram(4, self.table4_frame)
        canvas2 = self.pie_diagram(5, self.table4_frame)
        canvas3 = self.pie_diagram(6, self.table4_frame)

        canvas1.get_tk_widget().pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        canvas2.get_tk_widget().pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        canvas3.get_tk_widget().pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    # --- Einstellungen für ein Kuchendiagramm ---
    def pie_diagram(self, semester_number, master):
        semester_number = semester_number - 1
        fig, ax = plt.subplots(figsize=(4, 3))  
        fig.patch.set_facecolor('Gray')         

        werte = [
            self.controller.get_semester_progress(semester_number)[0],
            self.controller.get_semester_progress(semester_number)[1]
        ]
        labels = ['Offen', 'Abgeschlossen']

        wedges, texts, autotexts = ax.pie(
            werte,
            autopct='%1.1f%%',
            startangle=90
        )

        ax.set_title(f"{self.controller.get_semester_designation(semester_number)}")

        ax.legend(wedges, labels, loc="upper right")

        ax.axis('equal')

        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()
        canvas.get_tk_widget().configure(bg='Gray')  
        plt.close(fig)
        return canvas
    
    # --- Einstellungen für das Hinzufügen von Noten zu den Modulen ---
    def add_performance(self):
        self.top = tk.Toplevel()
        self.top_settings()

        table_frame = tk.Frame(self.top, bg="gray")
        table_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        table_frame.grid_columnconfigure(0, weight=3)
        table_frame.grid_columnconfigure(1, weight=1)
        table_frame.grid_columnconfigure(2, weight=1)

        headers = ["Modul:", "Note:", "Datum:"]
        
        # --- Eigener Header durch spalten-bug ---
        for col, text in enumerate(headers):
            label = tk.Label(table_frame, text=text, bg="#2C5C8C", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
            label.grid(row=0, column=col, sticky="nsew")

        # --- Modulauswahl vorbereiten ---
        all_modules = self.controller.get_all_open_modules()

        # --- Eingabefelder erstellen ---
        self.combo = ttk.Combobox(table_frame, values=all_modules, font=("Arial", 11), width=40)
        self.combo.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.entry_mark = tk.Entry(table_frame, font=("Arial", 11), width=15)
        self.entry_mark.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.entry_date = tk.Entry(table_frame, font=("Arial", 11), width=15)
        self.entry_date.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        save_button = tk.Button(self.top, text="Speichern", command=self.save, font=("Arial", 11), bg="#2C5C8C", fg="white")
        save_button.pack(pady=10)

    # --- Speicherungsverfahren nach dem drücken des Speicher-Knopfs ---
    def save(self):
        module_name = self.combo.get()
        try:
            mark_input = self.entry_mark.get().replace(",", ".")
            mark = float(mark_input)
            date = datetime.strptime(self.entry_date.get(), "%d.%m.%Y")
        except Exception as e:
            mb.showerror("Fehler", f"Ungültige Eingabe: {e}")
            return

        self.controller.update_performance(module_name, mark, date)
        self.top.destroy()
        self.update_display()

    # --- Einstellungen für das 2. Fenster ---
    def top_settings(self):
        width = 800
        height = 200

        x = int((self.get_screen_width() - width)/2)
        y = int((self.get_screen_height() - height)/2)

        self.top.title("Hinzufügen einer neuen Note")
        self.top.geometry(f"{width}x{height}+{x}+{y}")
        self.top.configure(bg="Lightgray")

    # --- Update der Kompletten Übersicht ---
    def update_display(self):
        self.update_progressbar()

        # --- Lösche Tabellen-Frames ---
        for table_frame_attr in ['table1_frame', 'table2_frame', 'table3_frame', 'table4_frame']:
            if hasattr(self, table_frame_attr):
                getattr(self, table_frame_attr).destroy()

        # --- Lösche auch den Hinzufügen-Button ---
        if hasattr(self, 'add_performance_button'):
            self.add_performance_button.pack_forget()

        # --- Neu erstellen ---
        self.create_table1()
        self.create_table2()
        self.create_table3()
        self.create_table4()

        # --- Button wieder ganz unten hinzufügen ---
        self.add_performance_button.pack()

    # --- Update der Progressbar ---
    def update_progressbar(self):
        reached = self.controller.get_metrics()["reached_ects"]
        total = self.controller.get_metrics()["total_ects"]
        progress_percent = self.controller.get_metrics()["progress_percent"]

        self.progress_bar['value'] = reached
        self.progress_bar['maximum'] = total

        self.progress_label.config(text=f"{progress_percent}%")

    # --- Einstellungen was beim schließen passiert ---
    def on_closing(self):
        self.get_root().quit()
        self.get_root().destroy()

    # --- Startet den Mainloop ---
    def run(self):
        # Tkinter mainloop starten
        self._root.mainloop()
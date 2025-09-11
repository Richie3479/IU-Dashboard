class Semester:
    def __init__(self, designation:str):
        self._designation = designation
        self._modules = []

    def add_module(self, module):
        return self._modules.append(module)
    
    def get_designation(self):
        return self._designation
    
    def get_modules(self):
        return self._modules
    
    # --- Gibt die ANzahl der Offenen und Angeschlossenen Module in einem Semester ---
    def get_progress(self):
        open_modules = 0
        finished_modules = 0

        for module in self.get_modules():
            if module.get_status() == "Abgeschlossen":
                finished_modules += 1
            elif module.get_status() == "Offen":
                open_modules += 1

        return open_modules, finished_modules
    

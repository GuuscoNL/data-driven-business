import customtkinter as ctk
from predictionFrame import PredictionFrame


WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1200

"""
Visualisaties:
Welke plekken de meeste storingsduur hebben
Per geo code de storingsduur, aantal storingen en de gemiddelde storingsduur, aantal storingen per maand
"""

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Zet de cursor op watch (laad cursor)
        self.config(cursor="watch")
        self.update()

        # Maak het window
        self.title("ProRail dashboard")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(True, True)
        self.minsize(300, 400)
        
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 5)
        self.grid_rowconfigure(0, weight = 1)
        
        self.prediction_frame = PredictionFrame(self)
        self.prediction_frame.grid(row = 0, column = 0, sticky = "wnse")
        
        # Zet de cursor op normaal
        self.config(cursor="")
        self.update()
    
if __name__ == "__main__":
    app = App()
    app.mainloop()
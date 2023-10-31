import customtkinter as ctk

import pandas as pd

"""
Visualisaties:
Welke plekken de meeste storingsduur hebben
Per geo code de storingsduur, aantal storingen en de gemiddelde storingsduur, aantal storingen per maand
"""

class VisualizationFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Grid
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 2)
        
        self.top_frame()
        
        self.bottom_frame()
        

    
    def top_frame(self):
        self.top_tab_view = ctk.CTkTabview(self)
        self.top_tab_view.grid(row = 0, column = 0, sticky = "nesw")
        self.top_tab_view.propagate(False)
        
        self.top_tab_view.add("geo_code")
        self.top_tab_view.add("top storingen")
        
        self.top_geo_code_frame(self.top_tab_view.tab("geo_code"))
        self.top_malfunction_frame(self.top_tab_view.tab("top storingen"))
        
        
    def top_geo_code_frame(self, tab):
        self.geo_code_frame = ctk.CTkFrame(tab)
        self.geo_code_frame.pack(side="top", fill="both", expand=True)
        self.geo_code_frame.propagate(False)
        
        self.geo_code_frame.grid_columnconfigure(0, weight = 1)
        self.geo_code_frame.grid_columnconfigure(1, weight = 1)
        self.geo_code_frame.grid_rowconfigure(0, weight = 1)
        
        self.left_frame = ctk.CTkFrame(self.geo_code_frame)
        self.left_frame.grid(row = 0, column = 0, sticky = "nesw")
        
        self.left_frame.grid_columnconfigure(0, weight = 1)
        self.left_frame.grid_columnconfigure(1, weight = 1)
        self.left_frame.grid_rowconfigure(0, weight = 1)
        self.left_frame.grid_rowconfigure(1, weight = 1)
        self.left_frame.grid_rowconfigure(2, weight = 1)
        self.left_frame.grid_rowconfigure(3, weight = 1)
        self.left_frame.grid_rowconfigure(4, weight = 1)
        self.left_frame.grid_rowconfigure(5, weight = 1)
        
        self.geo_code_label = ctk.CTkLabel(self.left_frame, text="Geo code", font=("Arial", 18))
        self.geo_code_label.grid(row = 0, column = 0, sticky = "nesw")
        
        self.geo_code_entry = ctk.CTkEntry(self.left_frame)
        self.geo_code_entry.grid(row = 0, column = 1, sticky = "nesw")
        
        
     
        
        
        
        
        
        
        
        
        self.right_frame = ctk.CTkFrame(self.geo_code_frame)
        self.right_frame.grid(row = 0, column = 1, sticky = "nesw")
        
        # self.geo_code_entry = ctk.CTkEntry(self.geo_code_frame)
        # self.geo_code_entry.grid(row = 0, column = 0, sticky = "nesw")
        

        
    

    def top_malfunction_frame(self, tab):
        self.top_malfunction_frame = ctk.CTkFrame(tab)
        self.top_malfunction_frame.pack(side="top", fill="both", expand=True)
        self.top_malfunction_frame.propagate(False)
    

    def bottom_frame(self):
        self.visualization_tab_view = ctk.CTkTabview(self)
        self.visualization_tab_view.grid(row = 1, column = 0, sticky = "nesw")
        self.visualization_tab_view.propagate(False)
        
        self.visualization_tab_view.add("test")
        self.visualization_tab_view.add("test2")
        
        self.visualization_frame = ctk.CTkFrame(self.visualization_tab_view.tab("test"))
        self.visualization_frame.pack(side="top", fill="both", expand=True)
        self.visualization_frame.propagate(False)
        
        self.visualization_frame2 = ctk.CTkFrame(self.visualization_tab_view.tab("test2"))
        self.visualization_frame2.pack(side="top", fill="both", expand=True)
        self.visualization_frame2.propagate(False)



if __name__ == "__main__":
    from app import main
    main()
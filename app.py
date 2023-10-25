import customtkinter as ctk

WINDOW_HEIGHT = 700
WINDOW_WIDTH = 500



class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ProRail dashboard")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(True, True)
        self.minsize(300, 400)

        self.features = []
    
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 10)
        self.grid_rowconfigure(1, weight = 1)
        
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(row = 0, column = 0, sticky = "nesw")
        self.top_frame.propagate(False)
        
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.grid(row = 1, column = 0, sticky = "nesw")
        self.bottom_frame.propagate(False)

        # top_frame
        self.add_feature_input(self.top_frame, "test", "str")
        self.add_feature_input(self.top_frame, "test2", "str")
        self.add_feature_input(self.top_frame, "test3", "str")
        self.add_feature_input(self.top_frame, "test4", "str")
        self.add_feature_input(self.top_frame, "test5", "str")
        self.add_feature_input(self.top_frame, "test6", "str")
        self.add_feature_input(self.top_frame, "test7", "str")
        self.add_feature_input(self.top_frame, "test8", "str")
        self.add_feature_input(self.top_frame, "test9", "str")
        
        # bottom_frame
        self.result_frame = ctk.CTkFrame(self.bottom_frame, height=(WINDOW_HEIGHT//2)-50, width=WINDOW_WIDTH, border_color="grey", border_width=2)
        self.result_frame.pack(side="top", fill="x", pady=(30, 30), padx=(30, 30))
        self.result_frame.propagate(False)
        
        label = ctk.CTkLabel(self.result_frame, text="Duur van storing: .....", font=("Arial", 18))
        label.pack(side="top", pady=(30, 0))
    
        label = ctk.CTkLabel(self.result_frame, text="Herstel: --:-- ..-..-....", font=("Arial", 18))
        label.pack(side="bottom", pady=(0, 30))
    
    def add_feature_input(self, master, feature_name, feature_type):
        frame = ctk.CTkFrame(master)
        frame.pack(side="top", fill="x", pady=(10, 0))
        
        label = ctk.CTkLabel(frame, text=f"{feature_name}:", font=("Arial", 18))
        label.pack(side="left", fill="x", padx=(WINDOW_WIDTH / 13, 0))
        
        if feature_type == "str":
            input_field = ctk.CTkEntry(frame, width=200)
        else:
            assert False, f"Unknown feature type: `{feature_type}`"

        input_field.pack(side="right", fill="x", padx=(0, WINDOW_WIDTH / 13), pady=(5, 5))
        
        self.features.append((label, input_field))
        
        


app = App()
app.mainloop()
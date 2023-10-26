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

        self.features_input_fields = []
    
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
        features = [("test",  "str", ""),
                    ("test2", "option", list("SBETPKOGXIMAR")),
                    ("AAA",   "int", ""),
                    ("test4", "str", ""),
                    ("test5", "str", ""),
                    ("test6", "str", ""),
                    ("test7", "str", ""),
                    ("test8", "str", ""),
                    ("test9", "str", "")]

        for feature in features:
            self.add_feature_input(self.top_frame, feature)
        
        # bottom_frame
        self.result_frame = ctk.CTkFrame(self.bottom_frame, height=(WINDOW_HEIGHT//2)-50, width=WINDOW_WIDTH, border_color="grey", border_width=2)
        self.result_frame.pack(side="top", fill="x", pady=(30, 30), padx=(30, 30))
        self.result_frame.propagate(False)
        
        self.result_duration_label = ctk.CTkLabel(self.result_frame, text="Duur van storing: .....", font=("Arial", 18))
        self.result_duration_label.pack(side="top", pady=(20, 0))
    
        self.result_date_label = ctk.CTkLabel(self.result_frame, text="Herstel: --:-- ..-..-....", font=("Arial", 18))
        self.result_date_label.pack(side="top", pady=(20, 0))
    
        self.predict_button = ctk.CTkButton(self.result_frame, text="Voorspel", command=self.predict, font=("Arial", 18))
        self.predict_button.pack(side="bottom", pady=(0, 20))
    
    def add_feature_input(self, master, feature):
        feature_name, feature_type = feature[0], feature[1]
        
        frame = ctk.CTkFrame(master)
        frame.pack(side="top", fill="x", pady=(10, 0))
        
        label = ctk.CTkLabel(frame, text=f"{feature_name}:", font=("Arial", 18))
        label.pack(side="left", fill="x", padx=(WINDOW_WIDTH / 13, 0))
        
        if feature_type == "str" or feature_type == "int":
            input_field = ctk.CTkEntry(frame, width=200)

        elif feature_type == "option":
            input_field = ctk.CTkOptionMenu(frame, values=feature[2])

        else:
            assert False, f"Unknown feature type: `{feature_type}`"

        input_field.pack(side="right", fill="x", padx=(0, WINDOW_WIDTH / 13), pady=(5, 5))
        
        self.features_input_fields.append((label, input_field))
    
    def predict(self):
        print("predicted")

app = App()
app.mainloop()
import customtkinter as ctk
import pickle
import pandas as pd

WINDOW_HEIGHT = 700
WINDOW_WIDTH = 500

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

        # Maak de grid
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 10)
        self.grid_rowconfigure(1, weight = 1)
        
        self.features_input_fields = {}

        self.load_data()
        
        # Main frames
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(row = 0, column = 0, sticky = "nesw")
        self.top_frame.propagate(False)
        
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.grid(row = 1, column = 0, sticky = "nesw")
        self.bottom_frame.propagate(False)

        # top_frame
        self.features = self.get_features()
        
        for feature in self.features:
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
        
        # Zet de cursor op normaal
        self.config(cursor="")
        self.update()


    def get_features(self):
        
        # remove the target column
        model_df_copy = self.model_df_raw.copy().drop(["anm_tot_fh"], axis=1)
        
        features = []
        
        while len(model_df_copy.columns) > 0:

            first_colm = model_df_copy.columns[0]

            # Krijg het begin van de naam van de kolom
            column_start = "_".join(first_colm.split("_")[:-1])

            # Krijg alle kolommen die beginnen met de naam van dat kolom
            columns = [x for x in model_df_copy.columns if x.startswith(column_start)]
            features.append({"name": column_start, 
                             "type": "option", 
                             "options": [x.split("_")[-1] for x in columns]})
            
            # Verwijder de kolommen die al zijn toegevoegd en ga door naar de volgende kolom
            model_df_copy = model_df_copy.drop(columns, axis=1)
            
        return features

    def add_feature_input(self, master, feature):
        feature_name, feature_type = feature["name"], feature["type"]
        
        frame = ctk.CTkFrame(master)
        frame.pack(side="top", fill="x", pady=(10, 0))
        
        label = ctk.CTkLabel(frame, text=f"{feature_name}:", font=("Arial", 18))
        label.pack(side="left", fill="x", padx=(WINDOW_WIDTH / 13, 0))
        
        # Maak een input veld voor de feature gebaseerd op het type
        if feature_type == "str" or feature_type == "int":
            input_field = ctk.CTkEntry(frame, width=200)

        elif feature_type == "option":
            input_field = ctk.CTkOptionMenu(frame, values=feature["options"])

        else:
            assert False, f"Unknown feature type: `{feature_type}`"

        input_field.pack(side="right", fill="x", padx=(0, WINDOW_WIDTH / 13), pady=(5, 5))
        
        self.features_input_fields[feature_name] = input_field
    
    def predict(self):
        X = {}
        
        for feature in self.features:
            if feature["type"] == "option":
                # Zet alle opties op False
                for x in feature["options"]:
                    X[f"{feature['name']}_{x}"] = False
                
                # Zet de optie die is gekozen op True
                value = self.features_input_fields[feature["name"]].get()
                X[f"{feature['name']}_{value}"] = True
            else:
                assert False, f"Unknown feature type: `{feature['type']}`"

        X = pd.DataFrame(X, index=[0])

        predicted = self.model.predict(X)[0]
        self.result_duration_label.configure(text=f"Duur van storing: {round(predicted)} minuten")
    
    def load_data(self):
        # laad het model
        with open("models/DecisionTreeRegressor.pkl", "rb") as file:
            self.model = pickle.load(file)
        
        # Laad het model dat is gebruikt tijdens het fitten van het model
        self.model_df_raw = pd.read_csv("data/model_df.csv", engine="pyarrow", index_col=0)

app = App()
app.mainloop()
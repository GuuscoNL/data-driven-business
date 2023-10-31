import customtkinter as ctk
import pickle
import pandas as pd
from typing import Any
from functools import partial
from infoWindow import ToplevelInfoWindow, open_top_levels, feature_dictionary
import winsound
import datetime

class PredictionFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Importeer hier, omdat het anders een circulaire import wordt
        from app import WINDOW_HEIGHT, WINDOW_WIDTH
        
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 10)
        self.grid_rowconfigure(1, weight = 1)
        self.propagate(False)
        
        self.features_input_fields = {}

        self.load_data()
        
        # Top frames
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
    
        self.result_date_label = ctk.CTkLabel(self.result_frame, text="Verwachte herstel: --:-- ..-..-....", font=("Arial", 18))
        self.result_date_label.pack(side="top", pady=(20, 0))
    
        self.predict_button = ctk.CTkButton(self.result_frame, text="Voorspel", command=self.predict, font=("Arial", 18))
        self.predict_button.pack(side="bottom", pady=(0, 20))
        
    def get_features(self) -> list[dict[str, Any]]:
        """Haalt alle kolommen uit `data/model_df.csv` en maakt daar een lijst van 
        met dicts van de naam en het type van de feature moet de mogelijke opties. 
        Dit wordt gebruikt bij het maken van de input velden.

        Returns:
            list[dict[str, Any]]: de features met naam, type en de opties daarvoor.
        """
        
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

    def add_feature_input(self, master: ctk.CTkFrame, feature: dict[str, Any]) -> None:
        """Maakt een input veld voor een feature en voegt die toe aan de master frame.

        Args:
            master (ctk.CTkFrame): De master frame waar het input veld aan wordt toegevoegd.
            feature (dict[str, Any]): De feature met de naam, type en opties.
        """
        feature_name, feature_type = feature["name"], feature["type"]
        
        frame = ctk.CTkFrame(master)
        frame.pack(side="top", fill="x", pady=(10, 0))
        
        label = ctk.CTkLabel(frame, text=f"{feature_name}:", font=("Arial", 18))
        label.pack(side="left", fill="x", padx=(10, 0))
        
        # Maak een input veld voor de feature gebaseerd op het type
        if feature_type == "str" or feature_type == "int":
            input_field = ctk.CTkEntry(frame, width=200)

        elif feature_type == "option":
            input_field = ctk.CTkOptionMenu(frame, values=feature["options"])
            
            if feature_dictionary.get(feature_name, None) is not None:
                info_button = ctk.CTkButton(frame, text="i", width=30 ,command=partial(self.open_top_level, feature_name, feature["options"]), font=("Arial", 18, "bold"))
            else:
                info_button = None

        else:
            assert False, f"Unknown feature type: `{feature_type}`"

        if info_button is not None: info_button.pack(side="right", padx=(5, 5))
        input_field.pack(side="right", fill="x", pady=(5, 5))
        
        self.features_input_fields[feature_name] = input_field
    
    def open_top_level(self, feature_name: str, options: list[str]) -> None:
        """Opent een top level window met informatie over de feature.

        Args:
            feature_name (str): De naam van de feature waar informatie over wordt gegeven.
            options (list[str]): De opties van de feature.
        """
        if open_top_levels.get(feature_name, None) is None:
            open_top_levels[feature_name] = ToplevelInfoWindow(feature_name, options)
        else:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
    
    def predict(self) -> None:
        """Voorspelt de duur van de storing op basis van de ingevulde waardes in de input velden.
        """
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
        
        # Bereken de datum en tijd van het herstel
        date = datetime.datetime.now() + datetime.timedelta(minutes=predicted)
        self.result_date_label.configure(text=f"Verwachte herstel: {date.strftime('%H:%M %d-%m-%Y')}")
    
    def load_data(self) -> None:
        """Laad het model en de kolommen die zijn gebruikt tijdens het fitten van het model.
        """
        # laad het model
        with open("./models/DecisionTreeRegressor.pkl", "rb") as file:
            self.model = pickle.load(file)
        
        # Laad het model dat is gebruikt tijdens het fitten van het model
        self.model_df_raw = pd.read_csv("data/model_df.csv", index_col=0, nrows=0)

if __name__ == "__main__":
    from app import main
    main()
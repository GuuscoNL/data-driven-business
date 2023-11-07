import customtkinter as ctk
import pandas as pd
from typing import Any
from functools import partial
from infoWindow import ToplevelInfoWindow, open_top_levels, feature_dictionary
import datetime
import json

feature_encodings = json.load(open("data/feature_encodings.json", "r"))


class PredictionFrame(ctk.CTkFrame):
    def __init__(self, model, model_df_raw, predict_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Importeer hier, omdat het anders een circulaire import wordt
        from app import WINDOW_HEIGHT, WINDOW_WIDTH
        
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 10)
        self.grid_rowconfigure(1, weight = 1)
        self.propagate(False)
        self.model = model
        self.model_df_raw = model_df_raw
        self.predict_callback = predict_callback
        
        self.features_input_fields = {}
        
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
        
    def get_features(self):
        """Haalt alle kolommen uit `data/model_df.csv` en maakt daar een lijst van 
        met dicts van de naam en het type van de feature moet de mogelijke opties. 
        Dit wordt gebruikt bij het maken van de input velden.

        Returns:
            list[dict[str, Any]]: de features met naam, type en de opties daarvoor.
        """
        
        # verwidjer de target kolom
        model_df_copy = self.model_df_raw.copy().drop(["anm_tot_fh"], axis=1)
        
        features = []
        #TODO: geo_code met entry ipv optionmenu
        
        for column in model_df_copy.columns:

            # Krijg het begin van de naam van de kolom
            column_name_split = column.split("_")
            column_start = "_".join(column_name_split[:-1])
            
            # Eindigt de kolom naam op "enc" dan is het een encoded feature
            if column_name_split[-1] == "enc":
                columns = [column]
                
                if (enc := feature_encodings.get(column_start, None)) is not None:
                    enc_keys = list(enc.keys())

                    if enc_keys[0].isnumeric():
                        enc_keys = sorted(enc_keys, key=lambda x: int(x))
                    
                    if column_start == "techn_veld":
                        features.append({"name": column_start, 
                                    "type": "enc_option", 
                                    "options": enc_keys})
                    else:
                        features.append({"name": column_start, 
                                        "type": "enc", 
                                        "options": enc_keys})
                else:
                    assert False, f"Unknown encoded feature: `{column_start}`"
                
            # Begint de kolom naam met "stm" dan is het niet een encoded feature
            elif column_name_split[0] == "stm":
                columns = [column]
                feature_name = "_".join(column_name_split[1:])
                if column == "stm_prioriteit":
                    features.append({"name": feature_name, 
                                    "type": "option", 
                                    "options": ["1", "2", "4", "5", "8", "9"]})
                else:
                    features.append({"name": feature_name, 
                                "type": "int", 
                                "options": []})
                
            # Geen idee wat het is dus geef een error
            else:
                assert False, f"Unknown column name: `{column}`"
            
            # Verwijder de kolommen die al zijn toegevoegd en ga door naar de volgende kolom
            model_df_copy = model_df_copy.drop(columns, axis=1)
            
        return features

    def add_feature_input(self, master: ctk.CTkFrame, feature) -> None:
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
        
        do_entry = feature_type == "str" or feature_type == "int" or feature_type == "enc"
        do_option = feature_type == "option" or feature_type == "enc_option"
        
        # Maak een input veld voor de feature gebaseerd op het type
        info_button = None
        if do_entry:
            input_field = ctk.CTkEntry(frame, width=200)

            if feature_dictionary.get(feature_name, None) is not None:
                info_button = ctk.CTkButton(frame, text="i", width=30 ,command=partial(self.open_top_level, feature_name, feature["options"]), font=("Arial", 18, "bold"))

        elif do_option:
            input_field = ctk.CTkOptionMenu(frame, values=feature["options"])
            
            if feature_dictionary.get(feature_name, None) is not None:
                info_button = ctk.CTkButton(frame, text="i", width=30 ,command=partial(self.open_top_level, feature_name, feature["options"]), font=("Arial", 18, "bold"))

        else:
            assert False, f"Unknown feature type: `{feature_type}`"

        if info_button is not None: info_button.pack(side="right", padx=(5, 5))
        input_field.pack(side="right", fill="x", pady=(5, 5))
        
        self.features_input_fields[feature_name] = input_field
    
    def open_top_level(self, feature_name: str, options) -> None:
        """Opent een top level window met informatie over de feature.

        Args:
            feature_name (str): De naam van de feature waar informatie over wordt gegeven.
            options (list[str]): De opties van de feature.
        """
        if open_top_levels.get(feature_name, None) is None:
            open_top_levels[feature_name] = ToplevelInfoWindow(feature_name, options)
    
    def predict(self) -> None:
        """Voorspelt de duur van de storing op basis van de ingevulde waardes in de input velden.
        """
        X = {}
        
        for feature in self.features:
            feature_type = feature["type"]
            feature_name = feature["name"]

            if feature_type == "option":
                if feature_name == "prioriteit":

                    X[f'stm_{feature_name}'] = int(self.features_input_fields[feature_name].get())
                else:
                    assert False, f"Unknown feature name with type `option`: `{feature_name}`"

            elif feature_type == "enc":
                value = self.features_input_fields[feature_name].get()
                if feature_encodings[feature_name].get(value, None) is None:
                    if value == "": value = " "
                    self.result_duration_label.configure(text=f"Duur van storing:\n'{value}' is geen geldige optie voor {feature_name}")
                    return
                X[f"{feature_name}_enc"] = feature_encodings[feature_name][value]
            
            elif feature_type == "enc_option":
                value = self.features_input_fields[feature_name].get()
                X[f"{feature_name}_enc"] = feature_encodings[feature_name][value]

            elif feature_type == "int":
                value = self.features_input_fields[feature_name].get()
                
                # check if input is a number
                if not value.isnumeric():
                    self.result_duration_label.configure(text=f"Duur van storing:\n'{value}' is geen geheel getal of is niet positief zijn")
                    return
                
                X[f'stm_{feature_name}'] = int(value)
                
            else:
                assert False, f"Unknown feature type: `{feature['type']}`"

        X = pd.DataFrame(X, index=[0])

        predicted = self.model.predict(X)[0]
        self.result_duration_label.configure(text=f"Duur van storing: {round(predicted)} minuten")
        
        # Bereken de datum en tijd van het herstel
        date = datetime.datetime.now() + datetime.timedelta(minutes=predicted)
        self.result_date_label.configure(text=f"Verwachte herstel: {date.strftime('%H:%M %d-%m-%Y')}")
        
        self.predict_callback(X)

if __name__ == "__main__":
    from app import main
    main()
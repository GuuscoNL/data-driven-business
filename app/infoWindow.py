import customtkinter as ctk
import json

open_top_levels = {}

feature_dictionary = json.load(open("./feature_dictionaries.json", "r"))

class ToplevelInfoWindow(ctk.CTkToplevel):
    def __init__(self, feature, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f"450x500")
        self.title(f"Informatie over {feature}")
        
        # make sure the window is on top of the main window
        self.attributes("-topmost", True)
        self.feature = feature
        
        #TODO: add scrollbar
        feature_dict = feature_dictionary.get(feature, None)
        if feature_dict is None:
            feature_dict = "Geen informatie beschikbaar"
        else:
            feature_dict = "\n".join([f"{key}: {value}" for key, value in feature_dict.items() if key in options])

        # size label to fit text
        
        self.label = ctk.CTkLabel(self, text=feature_dict, font=("Arial", 18), justify="left")
        self.label.pack(padx=20, pady=20)

        
        # add button to close window
        self.close_button = ctk.CTkButton(self, text="Sluiten", command=self.on_destroy)
        self.close_button.pack(pady=20, side="bottom")
        # on destroy set the open_top_levels[feature] to None
        self.protocol("WM_DELETE_WINDOW", self.on_destroy)
    
    def on_destroy(self):
        open_top_levels[self.feature] = None
        self.destroy()
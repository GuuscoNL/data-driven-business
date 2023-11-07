import customtkinter as ctk
import json

open_top_levels = {}

feature_dictionary = json.load(open("data/feature_dictionaries.json", "r"))

class ToplevelInfoWindow(ctk.CTkToplevel):
    def __init__(self, feature, options, callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(f"Informatie over {feature}")
        
        # make sure the window is on top of the main window
        self.attributes("-topmost", True)
        self.callback = callback
        self.feature = feature
        
        self.scrollbar_frame = ctk.CTkScrollableFrame(self)
        self.scrollbar_frame.pack(side="top", fill="both", expand=True)
        
        
        feature_dict = feature_dictionary.get(feature, None)
        feature_dict_str = ""
        
        # sorteer de opties op nummer als het nummers zijn
        if options[0].isnumeric():
            options = sorted(options, key=lambda x: int(x))
            # remove .0 from numbers
            options = [str(option).replace(".0", "") for option in options]
        
        if feature_dict is None:
            feature_dict_str = "Geen informatie beschikbaar"
        else:
            for option in options:
                if option not in feature_dict:
                    feature_dict_str += f"{option}: !Geen informatie beschikbaar!\n"
                else:
                    feature_dict_str += f"{option}: {feature_dict[option]}\n"

        height = len(feature_dict_str.split("\n"))
        width = max([len(line) for line in feature_dict_str.split("\n")])
        self.geometry(f"{width*9+50}x{min(height*21+130, 500)}")
        # size label to fit text
        
        self.label = ctk.CTkLabel(self.scrollbar_frame, text=feature_dict_str, font=("Arial", 18), justify="left")
        self.label.pack(padx=20, pady=20)

        
        # add button to close window
        self.close_button = ctk.CTkButton(self, text="Sluiten", command=self.on_destroy)
        self.close_button.pack(pady=20, side="bottom")
        # on destroy set the open_top_levels[feature] to None
        self.protocol("WM_DELETE_WINDOW", self.on_destroy)
    
    def on_destroy(self):
        open_top_levels[self.feature] = None
        if self.callback is not None:
            self.callback()
        self.destroy()

if __name__ == "__main__":
    from app import main
    main()
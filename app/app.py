import customtkinter as ctk
from predictionFrame import PredictionFrame
from visualization import VisualizationFrame
import pickle
import pandas as pd
import threading

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1400

cols_to_use = [
    '#stm_sap_meldnr',
    # 'stm_mon_nr',
    # 'stm_vl_post',
    # 'stm_sap_meld_ddt',
    # 'stm_sap_meldtekst_lang',
    # 'stm_sap_meldtekst',
    'stm_geo_mld',
    # 'stm_geo_mld_uit_functiepl',
    # 'stm_equipm_nr_mld',
    # 'stm_equipm_soort_mld',
    # 'stm_equipm_omschr_mld',
    # 'stm_km_van_mld',
    # 'stm_km_tot_mld',
    # 'stm_prioriteit',
    # 'stm_status_melding_sap',
    # 'stm_aanngeb_ddt',
    # 'stm_oh_pg_gst',
    # 'stm_geo_gst',
    # 'stm_geo_gst_uit_functiepl',
    # 'stm_equipm_nr_gst',
    # 'stm_equipm_soort_gst',
    # 'stm_equipm_omschr_gst',
    # 'stm_km_van_gst',
    # 'stm_km_tot_gst',
    # 'stm_oorz_groep',
    'stm_oorz_code',
    # 'stm_oorz_tkst',
    'stm_fh_ddt',
    # 'stm_fh_status',
    # 'stm_sap_storeind_ddt',
    # 'stm_tao_indicator',
    # 'stm_tao_indicator_vorige',
    # 'stm_tao_soort_mutatie',
    # 'stm_tao_telling_mutatie',
    # 'stm_tao_beinvloedbaar_indicator',
    # 'stm_evb',
    # 'stm_sap_melddatum',
    # 'stm_sap_meldtijd',
    # 'stm_contractgeb_mld',
    # 'stm_functiepl_mld',
    # 'stm_techn_mld',
    # 'stm_contractgeb_gst',
    # 'stm_functiepl_gst',
    # 'stm_techn_gst',
    # 'stm_aanngeb_dd',
    # 'stm_aanngeb_tijd',
    # 'stm_aanntpl_dd',
    # 'stm_aanntpl_tijd',
    # 'stm_arbeid',
    # 'stm_progfh_in_datum',
    # 'stm_progfh_in_tijd',
    # 'stm_progfh_in_invoer_dat',
    # 'stm_progfh_in_invoer_tijd',
    # 'stm_progfh_in_duur',
    # 'stm_progfh_gw_tijd',
    # 'stm_progfh_gw_lwd_datum',
    # 'stm_progfh_gw_lwd_tijd',
    # 'stm_progfh_gw_duur',
    # 'stm_progfh_gw_teller',
    # 'stm_afspr_aanvangdd',
    # 'stm_afspr_aanvangtijd',
    'stm_fh_dd',
    # 'stm_fh_tijd',
    'stm_fh_duur',
    # 'stm_reactie_duur',
    # 'stm_sap_storeinddatum',
    # 'stm_sap_storeindtijd',
    # 'stm_oorz_tekst_kort',
    # 'stm_pplg_van',
    # 'stm_pplg_naar',
    # 'stm_dstrglp_van',
    # 'stm_dstrglp_naar'
]

#TODO: Nederlandse comments
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Zet de cursor op watch (laad cursor)
        self.config(cursor="watch")
        self.update()
        self.propagate(False)

        # Maak het window
        self.title("ProRail dashboard")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(True, True)
        self.minsize(300, 400)
        
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 2)
        self.grid_rowconfigure(0, weight = 1)
        
        # make label to say 
        self.loading_label_model = ctk.CTkLabel(self, text="Laden model...", font=("Arial", 18))
        # pack in middle of frame
        self.loading_label_model.grid(row = 0, column = 0, sticky = "nesw")
        
        self.loading_label_data = ctk.CTkLabel(self, text="Laden data...", font=("Arial", 18))
        # pack in middle of frame
        self.loading_label_data.grid(row = 0, column = 1, sticky = "nesw")
        
        self.update()
        
        self.loading_label_model.destroy()
        
        import time
        start_time = time.time()
        
        #load data in thread
        model_thread = threading.Thread(target=self.load_model)
        model_thread.start()
        
        data_thread = threading.Thread(target=self.load_data)
        data_thread.start()
        
        model_thread.join()
        data_thread.join()
        
        print(f"Total time to load data and model: {(time.time() - start_time):.4f}")
        
        self.prediction_frame = PredictionFrame(self.model, self.model_df_raw, self.predict_callback, self)
        self.prediction_frame.grid(row = 0, column = 0, sticky = "wnse")
        
        self.update()
        self.loading_label_model.destroy()
        
        self.visualization_frame = VisualizationFrame(self.model, self.model_df_raw, self.data, self)
        self.visualization_frame.grid(row = 0, column = 1, sticky = "wnse")
        # Zet de cursor op normaal
        self.config(cursor="")
        self.update()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    
    def load_model(self) -> None:
        """Laad het model en de kolommen die zijn gebruikt tijdens het fitten van het model.
        """
        print("loading model...")
        # laad het model in a thread
        
        def on_model_thread():
            print("   model loading...")
            with open("./models/DecisionTreeRegressor.pkl", "rb") as file:
                self.model = pickle.load(file)
            print("   model loading done!")
        
        # Laad het model dat is gebruikt tijdens het fitten van het model
        def on_model_df_thread():
            print("   model_df loading...")
            self.model_df_raw = pd.read_csv("data/model_df.csv", index_col=0, engine="pyarrow")
            print("   model_df loading done!")
            
        model_thread = threading.Thread(target=on_model_thread)
        model_df_thread = threading.Thread(target=on_model_df_thread)
        model_thread.start()
        model_df_thread.start()
        
        model_thread.join()
        model_df_thread.join()
        
        print("model loaded")
        
    def load_data(self) -> None:
        print("loading data...")
        self.data = pd.read_csv("./data/sap_storing_data_hu_project.csv", index_col=0, engine="pyarrow", usecols=cols_to_use)
        
        # Remove .0 from geocode column
        print("data loaded, cleaning data...")
        self.data["stm_geo_mld"] = self.data["stm_geo_mld"].astype(str).replace(".0", "", regex=True)
        
        self.data.dropna(subset=["stm_geo_mld", "stm_fh_ddt"], inplace=True)
        
        # make sure the date columns are datetime
        self.data['stm_fh_ddt'] = pd.to_datetime(self.data['stm_fh_ddt'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
        
        print("Data cleaned")
        
    def predict_callback(self, X):
        self.visualization_frame.update_prediction(X)

    def on_closing(self):
        # Dit is gedaan, omdat er anders invalid command gedoe krijgt...
        self.withdraw()
        self.quit()

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
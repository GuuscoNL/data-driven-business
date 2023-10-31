import customtkinter as ctk
from predictionFrame import PredictionFrame
from visualization import VisualizationFrame
import pandas as pd
import asyncio

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1300

data = None

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
    'stm_prioriteit',
    # 'stm_status_melding_sap',
    # 'stm_aanngeb_ddt',
    # 'stm_oh_pg_gst',
    'stm_geo_gst',
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
    'stm_contractgeb_mld',
    # 'stm_functiepl_mld',
    'stm_techn_mld',
    # 'stm_contractgeb_gst',
    # 'stm_functiepl_gst',
    'stm_techn_gst',
    # 'stm_aanngeb_dd',
    # 'stm_aanngeb_tijd',
    'stm_aanntpl_dd',
    'stm_aanntpl_tijd',
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
    'stm_fh_tijd',
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
        self.grid_columnconfigure(1, weight = 3)
        self.grid_rowconfigure(0, weight = 1)
        
        self.prediction_frame = PredictionFrame(self)
        self.prediction_frame.grid(row = 0, column = 0, sticky = "wnse")
        
        self.load_data_button = ctk.CTkButton(self, text="Laad data", command=self.load_visualization, font=("Arial", 18))
        self.load_data_button.grid(row = 0, column = 1, sticky = "wnse")
        
        # Zet de cursor op normaal
        self.config(cursor="")
        self.update()

    def load_visualization(self):
        self.load_data_button.destroy()
        
        # toplevel with massage that data is loading
        self.loading_window = ctk.CTkToplevel(self)
        self.loading_window.title("Data laden...")
        self.loading_window.geometry("300x100")
        self.loading_window.resizable(False, False)
        self.loading_window.propagate(False)
        
        self.loading_window.grid_columnconfigure(0, weight = 1)
        self.loading_window.grid_rowconfigure(0, weight = 3)
        self.loading_window.grid_rowconfigure(1, weight = 1)
        
        self.loading_label = ctk.CTkLabel(self.loading_window, text="Data wordt geladen...", font=("Arial", 18))
        self.loading_label.grid(row = 0, column = 0, sticky = "nesw")
        
        self.loading_progressbar = ctk.CTkProgressBar(self.loading_window, width=200, mode="determinate")
        self.loading_progressbar.grid(row = 1, column = 0, sticky = "nesw")
        
        self.loading_window.attributes("-topmost", True)
        self.loading_window.update()

        # Load data in a thread and when done destroy the loading window and create the visualization frame
        import threading
        thread = threading.Thread(target=self.load_data(), daemon=True)
        thread.start()
        
    
    def load_data(self):

        total_rows = 0
        global data
        for chunk in pd.read_csv("./data/sap_storing_data_hu_project.csv", chunksize=30000, index_col=0, low_memory=False, usecols=cols_to_use):
            if data is None:
                data = chunk
            else:
                data = pd.concat([data, chunk])
            total_rows += len(chunk)
            self.loading_progressbar.set(total_rows/898526)
            self.loading_window.update()

        self.loading_window.destroy()
        
        self.visualization_frame = VisualizationFrame(self)
        self.visualization_frame.grid(row = 0, column = 1, sticky = "wnse")

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
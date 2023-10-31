import customtkinter as ctk
import pandas as pd
"""
Visualisaties:
Welke plekken de meeste storingsduur hebben
Per geo code de storingsduur, aantal storingen en de gemiddelde storingsduur, aantal storingen per maand
"""

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

class VisualizationFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.propagate(False)
        data = pd.read_csv("./data/sap_storing_data_hu_project.csv", index_col=0, engine="pyarrow", usecols=cols_to_use)
        print(data.head())
        
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
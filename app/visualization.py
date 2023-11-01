import customtkinter as ctk
import tkinter as tk
import pandas as pd
import json

feature_dictionary = json.load(open("./feature_dictionaries.json", "r"))

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

        # add label to tell that the data is loading
        self.loading_label = ctk.CTkLabel(self, text="Loading data...", font=("Arial", 30))
        self.loading_label.pack(side="top", fill="both", expand=True)

        self.propagate(False)
        
    def init(self):
        self.data = pd.read_csv("./data/sap_storing_data_hu_project.csv", index_col=0, engine="pyarrow", usecols=cols_to_use)
        self.total_data = len(self.data)
        
        
        # Remove .0 from geocode column
        self.data["stm_geo_mld"] = self.data["stm_geo_mld"].astype(str).replace("\.0", "", regex=True)
        
        self.data.dropna(subset=["stm_geo_mld", "stm_fh_ddt"], inplace=True)
        
        # make sure the date columns are datetime
        self.data['stm_fh_ddt'] = pd.to_datetime(self.data['stm_fh_ddt'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
        
        # Grid
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 2)
        self.grid_rowconfigure(1, weight = 6)
        
        self.loading_label.destroy()

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
        self.geo_code_frame.pack(side="top", fill="both")
        self.geo_code_frame.propagate(False)
        
        self.geo_code_sub_frame = ctk.CTkFrame(self.geo_code_frame, fg_color="#2b2b2b")
        self.geo_code_sub_frame.pack(side="top")
        
        self.geo_code_label = ctk.CTkLabel(self.geo_code_sub_frame, text="Geo code: ", font=("Arial", 18))
        self.geo_code_label.pack( side="left")

        self.geo_code_entry = ctk.CTkEntry(self.geo_code_sub_frame, placeholder_text="559")
        self.geo_code_entry.pack(side="left", fill="both")
        
        self.geo_code_mean_label = ctk.CTkLabel(self.geo_code_frame, text="Gemiddelde storingsduur: ", font=("Arial", 18))
        self.geo_code_mean_label.pack(side="top", fill="both")
        
        self.geo_code_mean_month_label = ctk.CTkLabel(self.geo_code_frame, text="Gemiddelde aantal storingen per maand: ", font=("Arial", 18))
        self.geo_code_mean_month_label.pack(side="top", fill="both")
        
        self.geo_code_total_label = ctk.CTkLabel(self.geo_code_frame, text="Totaal aantal storingen: ", font=("Arial", 18))
        self.geo_code_total_label.pack(side="top", fill="both")
        
        self.geo_code_most_cause_label = ctk.CTkLabel(self.geo_code_frame, text="Meest voorkomende oorzaak: ", font=("Arial", 18))
        self.geo_code_most_cause_label.pack(side="top", fill="both")
        
        # add button
        self.geo_code_button = ctk.CTkButton(self.geo_code_frame, text="Bereken", command=self.on_geo_code_button_click)
        self.geo_code_button.pack(side="top")
        
    def on_geo_code_button_click(self):
        geo_code = self.geo_code_entry.get()
        all_geo_codes = sorted(self.data["stm_geo_mld"].unique().tolist())
        
        # Check of de geocode valid is
        if not geo_code in all_geo_codes:
            # zorg dat de geocode entry rood wordt
            if geo_code == "":
                self.geo_code_entry.configure(text_color="white")
            else:
                self.geo_code_entry.configure(text_color="red")
            
            # leeg de labels
            self.geo_code_mean_label.configure(text="Gemiddelde storingsduur: ")
            self.geo_code_mean_month_label.configure(text="Gemiddelde aantal storingen per maand: ")
            self.geo_code_total_label.configure(text="Totaal aantal storingen: ")
            return
        
        self.geo_code_entry.configure(text_color="white")
        
        data_geo_code = self.data[self.data["stm_geo_mld"] == geo_code]
        
        #bereken de gemiddelde storingsduur voor de geocode
        geo_code_mean = data_geo_code["stm_fh_duur"].mean()
        geo_code_mean = round(geo_code_mean, 2)
        self.geo_code_mean_label.configure(text=f"Gemiddelde storingsduur: {geo_code_mean}")
        
        #bereken de gemiddelde aantal storingen per maand voor de geocode
        # verdeel de data in jaren
        data_geo_code["year"] = data_geo_code["stm_fh_ddt"].dt.year
        
        # voor elk jaar bereken de gemiddelde aantal storingen per maand
        
        geo_code_mean_per_month = round(data_geo_code.groupby('year')['stm_fh_duur'].count().mean()/12)
        self.geo_code_mean_month_label.configure(text=f"Gemiddelde aantal storingen per maand: {geo_code_mean_per_month}")
        
        #bereken het totaal aantal storingen voor de geocode
        geo_code_total = data_geo_code["stm_fh_duur"].count()
        self.geo_code_total_label.configure(text=f"Totaal aantal storingen: {geo_code_total}")
        
        # bereken de meest voorkomende oorzaak voor de geocode
        geo_code_most_cause = data_geo_code["stm_oorz_code"].value_counts().idxmax()
        self.geo_code_most_cause_label.configure(text=f"Meest voorkomende oorzaak: {geo_code_most_cause}")
        
    def top_malfunction_frame(self, tab):
        self.top_malfunction_frame = ctk.CTkFrame(tab)
        self.top_malfunction_frame.pack(side="top", fill="both", expand=True)
        self.top_malfunction_frame.propagate(False)

        self.total_mean_label = ctk.CTkLabel(self.top_malfunction_frame, text="Gemiddelde storingsduur: ", font=("Arial", 18))
        self.total_mean_label.pack(side="top", fill="both")
        
        self.total_mean_month_label = ctk.CTkLabel(self.top_malfunction_frame, text="Gemiddelde aantal storingen per maand: ", font=("Arial", 18))
        self.total_mean_month_label.pack(side="top", fill="both")
        
        self.total_total_label = ctk.CTkLabel(self.top_malfunction_frame, text="Totaal aantal storingen: ", font=("Arial", 18))
        self.total_total_label.pack(side="top", fill="both")
        
        self.total_most_cause_label = ctk.CTkLabel(self.top_malfunction_frame, text="Meest voorkomende oorzaak: ", font=("Arial", 18))
        self.total_most_cause_label.pack(side="top", fill="both")
        
        self.total_mean_label.configure(text=f"Gemiddelde storingsduur: {round(self.data['stm_fh_duur'].mean())} minuten")
        
        self.data["year"] = self.data["stm_fh_ddt"].dt.year
        
        self.total_mean_month_label.configure(text=f"Gemiddelde aantal storingen per maand: {round(self.data.groupby('year')['stm_fh_duur'].count().mean()/12)}")
        
        self.total_total_label.configure(text=f"Totaal aantal storingen: {self.total_data}")
        
        most_common_causes = self.data['stm_oorz_code'].value_counts().index.tolist()
        most_common_causes = [str(cause) for cause in most_common_causes]
        
        causes_to_ignore =["215", "221", "218", "135", "151", "298"]
        top_causes = []
        # ignore some causes
        for cause in most_common_causes:
            cause = cause.replace(".0", "")
            if len(top_causes) >= 5:
                break
            if cause not in causes_to_ignore:
                top_causes.append(cause)

        top_causes_str = ""
        for i, cause in enumerate(top_causes):
            info = feature_dictionary.get("oorz_code", {}).get(cause, "Geen informatie beschikbaar")
            top_causes_str += (f"{i+1}. {info}\n")
        
        self.total_most_cause_label.configure(text=f"Top 3 meest voorkomende oorzaak:\n{top_causes_str}")
    

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
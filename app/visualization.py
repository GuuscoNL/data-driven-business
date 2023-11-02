import customtkinter as ctk
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from infoWindow import ToplevelInfoWindow
from functools import partial
import pickle
import json

from PlotPrediction import plot_prediction

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

class VisualizationFrame(ctk.CTkFrame):
    def __init__(self, model, model_df_raw, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add label to tell that the data is loading
        self.loading_label = ctk.CTkLabel(self, text="Loading data...", font=("Arial", 30))
        self.loading_label.pack(side="top", fill="both", expand=True)
        self.propagate(False)
        self.info_window_is_open = False
        self.model = model
        self.model_df_raw = model_df_raw
        self.prediction_canvas = None
        
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
        self.geo_code_frame.pack(side="top", fill="both", expand=True)
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
        
        self.visualization_tab_view.add("Voorspelling")
        self.visualization_tab_view.add("Storingen per jaar")
        self.visualization_tab_view.add("Histogram storingsduur")
        self.visualization_tab_view.add("Vaak voorkomende oorzaken")
        
        self.visualization_frame = ctk.CTkFrame(self.visualization_tab_view.tab("Storingen per jaar"))
        self.visualization_frame.pack(side="top", fill="both", expand=True)
        self.visualization_frame.propagate(False)
        
        # make a plot that shows the amount of malfunctions per year
        self.data["year"] = self.data["stm_fh_ddt"].dt.year
        malfunction_per_year = self.data.groupby("year")["stm_fh_duur"].count()
        plt.style.use('grayscale')
        
        fig = plt.figure(figsize=(10, 5), dpi=100)
        plot = fig.add_subplot(111)
        plot.set_title("Aantal storingen per jaar")
        plot.set_xlabel("Jaar")
        plot.set_xticks(malfunction_per_year.index)
        plot.set_ylabel("Aantal storingen")
        plot.plot(malfunction_per_year.index, malfunction_per_year, marker="o", color="b")
        plot.grid(True, color="#d3d3d3")

        # show the plot in the frame
        canvas = FigureCanvasTkAgg(fig, master=self.visualization_frame)
        # make canvas dar mode
        canvas.draw()
        canvas.get_tk_widget().pack()
        
        self.visualization_frame2 = ctk.CTkFrame(self.visualization_tab_view.tab("Histogram storingsduur"))
        self.visualization_frame2.pack(side="top", fill="both", expand=True)
        self.visualization_frame2.propagate(False)
        
        # remove outliers via IQR methode
        Q1, Q3 = self.data["stm_fh_duur"].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        self.data = self.data[~((self.data["stm_fh_duur"] < (Q1 - 1.5 * IQR)) |(self.data["stm_fh_duur"] > (Q3 + 1.5 * IQR)))]
        
        # plot histogram of malfunction duration
        fig2 = plt.figure(figsize=(10, 4), dpi=100)
        plot2 = fig2.add_subplot(111)
        plot2.set_title("Histogram van storingsduur")
        plot2.set_xlabel("Storingsduur (minuten)")
        plot2.set_ylabel("Aantal storingen")
        plot2.hist(self.data["stm_fh_duur"], bins=100, color="b")
        plot2.grid(True, color="#d3d3d3")
        
        # show the plot in the frame
        canvas1 = FigureCanvasTkAgg(fig2, master=self.visualization_frame2)
        # make canvas dar mode
        canvas1.draw()
        canvas1.get_tk_widget().pack()
        
        
        # plot bar chart of most common causes
        self.visualization_frame3 = ctk.CTkFrame(self.visualization_tab_view.tab("Vaak voorkomende oorzaken"))
        self.visualization_frame3.pack(side="top", fill="both", expand=True)
        self.visualization_frame3.propagate(False)
        
        # plot how many times each cause occurs
        most_common_causes = self.data['stm_oorz_code'].value_counts().iloc[:20]
        most_common_causes = most_common_causes.sort_values(ascending=False)
        most_common_causes_keys = most_common_causes.index.astype(str).tolist()
        most_common_causes_values = most_common_causes.values.tolist()
        
        most_common_causes_keys = [key.replace(".0", "") for key in most_common_causes_keys]
        
        
        fig3 = plt.figure(figsize=(9, 4), dpi=100)
        plot3 = fig3.add_subplot(111)
        plot3.set_title("Vaak voorkomende oorzaken")
        plot3.set_xlabel("Oorzaak")
        plot3.set_ylabel("Aantal storingen")
        # Geeft warning maar werkt wel
        plot3.set_xticklabels(most_common_causes_keys, rotation=45)
        # X-axis is the cause, Y-axis is the amount of times it occurs
        plot3.bar(most_common_causes_keys, most_common_causes_values, color="b")
        plot3.grid(False)
        
        # show the plot in the frame
        canvas2 = FigureCanvasTkAgg(fig3, master=self.visualization_frame3)
        # make canvas dar mode
        canvas2.draw()
        canvas2.get_tk_widget().pack()
        
        # voeg info knop toe
        self.info_button = ctk.CTkButton(self.visualization_frame3, width=30, text="Oorzaak code dictionary", command=partial(self.open_top_level, most_common_causes_keys))
        self.info_button.pack(side="top")
        
        self.visualization_frame4 = ctk.CTkFrame(self.visualization_tab_view.tab("Voorspelling"))
        self.visualization_frame4.pack(side="top", fill="both", expand=True)
        self.visualization_frame4.propagate(False)

    
    def update_prediction(self, input):
        fig4, ax = plt.subplots(figsize=(12, 8))
        X = self.model_df_raw.drop("anm_tot_fh", axis=1)
        Y = self.model_df_raw["anm_tot_fh"]
        plot_prediction(self.model, input, fig4, ax, X, Y)
        
        # show the plot in the frame
        if self.prediction_canvas is not None:
            self.prediction_canvas.get_tk_widget().destroy()
        self.prediction_canvas = FigureCanvasTkAgg(fig4, master=self.visualization_frame4)
        # make canvas dar mode
        self.prediction_canvas.draw()
        self.prediction_canvas.get_tk_widget().pack()
    
    def open_top_level(self, options: list[str]) -> None:
        """Opent een top level window met informatie over de feature.

        Args:
            feature_name (str): De naam van de feature waar informatie over wordt gegeven.
            options (list[str]): De opties van de feature.
        """
        if not self.info_window_is_open:
            self.info_window = ToplevelInfoWindow("oorz_code", options, self.infoWindow_callback)
            self.info_window_is_open = not self.info_window_is_open

    def infoWindow_callback(self):
        # wordt aangeroepen wanneer de info window wordt gesloten
        self.info_window_is_open = False
        



if __name__ == "__main__":
    from app import main
    main()
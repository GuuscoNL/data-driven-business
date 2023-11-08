import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from infoWindow import ToplevelInfoWindow
from functools import partial
import pandas as pd
import json

from PlotPrediction import plot_prediction, get_95_interval

feature_dictionary = json.load(open("data/feature_dictionaries.json", "r"))

class VisualizationFrame(ctk.CTkFrame):
    def __init__(self, model, model_df_raw, data_tuple, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add label to tell that the data is loading
        self.propagate(False)
        self.info_window_is_open = False
        self.model = model
        self.model_df_raw = model_df_raw

        self.total_data = data_tuple[0]
        self.all_geo_codes = data_tuple[1]
        self.data = data_tuple[2]

        self.prediction_canvas = None
        self.causes_to_ignore =["215", "221", "218", "135", "151", "298"]

        
        
        # Grid
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 2)
        self.grid_rowconfigure(1, weight = 6)

        self.top_frame()
        
        self.bottom_frame()
    
    def top_frame(self):
        self.top_tab_view = ctk.CTkTabview(self)
        self.top_tab_view.grid(row = 0, column = 0, sticky = "nesw")
        self.top_tab_view.propagate(False)
        
        self.top_tab_view.add("Voorspelling")
        self.top_tab_view.add("Geo code")
        self.top_tab_view.add("Top storingen")
        
        self.prediction_frame(self.top_tab_view.tab("Voorspelling"))
        self.top_geo_code_frame(self.top_tab_view.tab("Geo code"))
        self.top_malfunction_frame(self.top_tab_view.tab("Top storingen"))
    
    def prediction_frame(self, tab):
        self.prediction_frame = ctk.CTkFrame(tab)
        self.prediction_frame.pack(side="top", fill="both", expand=True)
        self.prediction_frame.propagate(False)
        
        self.interval_label = ctk.CTkLabel(self.prediction_frame, text="In 95% van de gevallen zit de functie herstel duur tussen:\n...", font=("Arial", 24), justify="left")
        self.interval_label.pack(side="top", fill="both")
        
        self.RMSE_frame = ctk.CTkFrame(self.prediction_frame, fg_color="#2b2b2b")
        self.RMSE_frame.pack(side="top")
        self.RMSE_frame.propagate(False)

        self.RMSE_label = ctk.CTkLabel(self.RMSE_frame, text="Voorspellings RMSE: ...", font=("Arial", 24))
        self.RMSE_label.grid(row=0, column=0, sticky="nesw")
        
        # add info button to the left of the label
        self.info_button = ctk.CTkButton(self.RMSE_frame, text="i", width=30 ,command=self.open_RMSE_info, font=("Arial", 18, "bold"))
        self.info_button.grid(row=0, column=1, sticky="nesw")
        
    def open_RMSE_info(self):
        if not self.info_window_is_open:
            self.info_window = ctk.CTkToplevel(self)
            self.info_window.title("RMSE")
            self.info_window.geometry("600x200")
            self.info_window.propagate(False)
            self.info_window_is_open = not self.info_window_is_open
            
            self.info_window_label = ctk.CTkLabel(self.info_window, text="Root Mean Square Error (RMSE) is een maat voor \nde nauwkeurigheid van een voorspelling.\nHoe lager de RMSE, hoe beter de voorspelling.", font=("Arial", 18))
            self.info_window_label.pack(side="top", fill="both", padx=20, pady=20)
            
            # add button to close window
            self.close_button = ctk.CTkButton(self.info_window, text="Sluiten", command=self.on_info_window_close)
            self.close_button.pack(pady=20, side="bottom")
            
            # when the window is closed set the info_window_is_open to False
            self.info_window.attributes("-topmost", True)
            self.info_window.protocol("WM_DELETE_WINDOW", self.on_info_window_close)
    
    def on_info_window_close(self):
        self.info_window_is_open = False
        self.info_window.destroy()
        
    
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
        
        self.geo_code_median_label = ctk.CTkLabel(self.geo_code_frame, text="Mediaan storingsduur: ", font=("Arial", 18))
        self.geo_code_median_label.pack(side="top", fill="both")
        
        self.geo_code_mean_month_label = ctk.CTkLabel(self.geo_code_frame, text="Gemiddelde aantal storingen per maand: ", font=("Arial", 18))
        self.geo_code_mean_month_label.pack(side="top", fill="both")
        
        self.geo_code_total_label = ctk.CTkLabel(self.geo_code_frame, text="Totaal aantal storingen: ", font=("Arial", 18))
        self.geo_code_total_label.pack(side="top", fill="both")
        
        self.geo_code_most_cause_label = ctk.CTkLabel(self.geo_code_frame, text="Meest voorkomende oorzaak: ", font=("Arial", 18))
        self.geo_code_most_cause_label.pack(side="top", fill="both")
        
        # add button
        self.geo_code_button = ctk.CTkButton(self.geo_code_frame, text="Bereken", command=self.on_geo_code_button_click)
        self.geo_code_button.pack(side="top", pady=(10,0))
        
    def on_geo_code_button_click(self):
        geo_code = self.geo_code_entry.get()
        self.all_geo_codes = sorted(self.data["stm_geo_mld"].unique().tolist())
        
        # Check of de geocode valid is
        if  geo_code not in self.all_geo_codes:
            # zorg dat de geocode entry rood wordt
            if geo_code == "":
                self.geo_code_entry.configure(text_color="white")
            else:
                self.geo_code_entry.configure(text_color="red")
            
            # leeg de labels
            self.geo_code_median_label.configure(text="Mediaan storingsduur: ")
            self.geo_code_mean_month_label.configure(text="Gemiddelde aantal storingen per maand: ")
            self.geo_code_total_label.configure(text="Totaal aantal storingen: ")
            return
        
        self.geo_code_entry.configure(text_color="white")
        
        data_geo_code = self.data[self.data["stm_geo_mld"] == geo_code]
        
        #bereken de gemiddelde storingsduur voor de geocode
        geo_code_median = data_geo_code["stm_fh_duur"].median()
        self.geo_code_median_label.configure(text=f"Mediaan storingsduur: {int(geo_code_median//60)} uur en {int(geo_code_median%60)} minuten")
        
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
        geo_code_most_cause = data_geo_code["stm_oorz_code"].value_counts()
        
        geo_code_most_cause_str = "Geen informatie beschikbaar"
        # check if the cuase is not in the causes to ignore
        for cause in geo_code_most_cause.index:
            cause = str(cause).replace(".0", "")
            if cause not in self.causes_to_ignore:
                geo_code_most_cause_str = feature_dictionary.get("oorz_code", {}).get(str(cause), "Geen informatie beschikbaar")
                break
        
        self.geo_code_most_cause_label.configure(text=f"Meest voorkomende oorzaak:\n{str(geo_code_most_cause_str)}")
        
    def top_malfunction_frame(self, tab):
        self.top_malfunction_frame = ctk.CTkFrame(tab)
        self.top_malfunction_frame.pack(side="top", fill="both", expand=True)
        self.top_malfunction_frame.propagate(False)

        self.total_mean_label = ctk.CTkLabel(self.top_malfunction_frame, text="Mediaan storingsduur: ", font=("Arial", 18))
        self.total_mean_label.pack(side="top", fill="both")
        
        self.total_mean_month_label = ctk.CTkLabel(self.top_malfunction_frame, text="Gemiddelde aantal storingen per maand: ", font=("Arial", 18))
        self.total_mean_month_label.pack(side="top", fill="both")
        
        self.total_total_label = ctk.CTkLabel(self.top_malfunction_frame, text="Totaal aantal storingen: ", font=("Arial", 18))
        self.total_total_label.pack(side="top", fill="both")
        
        self.total_most_cause_label = ctk.CTkLabel(self.top_malfunction_frame, text="Meest voorkomende oorzaak: ", font=("Arial", 18), justify="left")
        self.total_most_cause_label.pack(side="top", fill="both")
        
        total_mean = self.data["stm_fh_duur"].median()
        # format H hour M minutes
        total_mean_str = f"{int(total_mean//60)} uur en {int(total_mean%60)} minuten"
        
        self.total_mean_label.configure(text=f"Mediaan storingsduur: {total_mean_str}")
        
        self.data["year"] = self.data["stm_fh_ddt"].dt.year
        
        self.total_mean_month_label.configure(text=f"Gemiddelde aantal storingen per maand: {round(self.data.groupby('year')['stm_fh_duur'].count().mean()/12)}")
        
        self.total_total_label.configure(text=f"Totaal aantal storingen: {self.total_data}")
        
        most_common_causes = self.data['stm_oorz_code'].value_counts().index.tolist()
        most_common_causes = [str(cause) for cause in most_common_causes]
        
        
        top_causes = []
        # ignore some causes
        for cause in most_common_causes:
            cause = cause.replace(".0", "")
            if len(top_causes) >= 5:
                break
            if cause not in self.causes_to_ignore:
                top_causes.append(cause)

        top_causes_str = ""
        for i, cause in enumerate(top_causes):
            info = feature_dictionary.get("oorz_code", {}).get(cause, "Geen informatie beschikbaar")
            top_causes_str += (f"{i+1}. {info}\n")
        
        self.total_most_cause_label.configure(text=f"Top 5 meest voorkomende oorzaken:\n{top_causes_str}")

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
        # only till year 2018
        malfunction_per_year = malfunction_per_year[:13]
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
        
        # where it is lower than 500 minuten
        duur = self.data[(self.data["stm_fh_duur"] > 5) & (self.data["stm_fh_duur"] < 480)]["stm_fh_duur"]
        
        # plot histogram of malfunction duration
        fig2 = plt.figure(figsize=(10, 5), dpi=100)
        plot2 = fig2.add_subplot(111)
        plot2.set_title("Histogram van storingsduur (5 tot 480 minuten)")
        plot2.set_xlabel("Storingsduur (minuten)")
        plot2.set_ylabel("Aantal storingen")
        plot2.hist(duur, bins=100, color="b")
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
        
        
        fig3 = plt.figure(figsize=(10, 5), dpi=100)
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
        self.info_button.pack(side="top", pady=(10,0))
        
        self.visualization_frame4 = ctk.CTkFrame(self.visualization_tab_view.tab("Voorspelling"))
        self.visualization_frame4.pack(side="top", fill="both", expand=True)
        self.visualization_frame4.propagate(False)

    
    def update_prediction(self, input):
        fig4, ax = plt.subplots(figsize=(12, 8))
        X = self.model_df_raw.drop("anm_tot_fh", axis=1)
        Y = self.model_df_raw["anm_tot_fh"]
        plot_prediction(self.model, input, ax, X, Y)
        
        # show the plot in the frame
        if self.prediction_canvas is not None:
            self.prediction_canvas.get_tk_widget().destroy()
        self.prediction_canvas = FigureCanvasTkAgg(fig4, master=self.visualization_frame4)
        # make canvas dar mode
        self.prediction_canvas.draw()
        self.prediction_canvas.get_tk_widget().pack()
        
        prediction_results = get_95_interval(self.model, input, X, Y)
        
        self.RMSE_label.configure(text=f"RMSE Voorspelling: {prediction_results['rmse']:.2f}")
        self.interval_label.configure(text=f"In 95% van de gevallen zit de functie herstel duur tussen:\n{prediction_results['interval'][0]:.2f} minuten en {prediction_results['interval'][1]:.2f} minuten")
        
        self.top_tab_view.set("Voorspelling")
        self.visualization_tab_view.set("Voorspelling")
    
    def open_top_level(self, options) -> None:
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
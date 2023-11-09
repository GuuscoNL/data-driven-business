import customtkinter as ctk
from predictionFrame import PredictionFrame
from visualization import VisualizationFrame
import pickle
import pandas as pd

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1400


#TODO: Nederlandse comments
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Zet de cursor op watch (laad cursor)
        self.config(cursor="watch")
        self.update()
        self.propagate(False)

        # Maak de window
        self.title("ProRail dashboard")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(True, True)
        self.minsize(300, 400)
        
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 2)
        self.grid_rowconfigure(0, weight = 1)
        
        # Laad labels
        self.loading_label_model = ctk.CTkLabel(self, text="Laden model...", font=("Arial", 18))
        self.loading_label_model.grid(row = 0, column = 0, sticky = "nesw")
        
        self.loading_label_data = ctk.CTkLabel(self, text="Laden data...", font=("Arial", 18))
        self.loading_label_data.grid(row = 0, column = 1, sticky = "nesw")
        
        # Update de window, zo dat de labels zichtbaar worden
        self.update()
        
        self.loading_label_model.destroy()
        
        import time
        start_time = time.time()
        
        self.load_data()
        
        print(f"Total time to load data and model: {(time.time() - start_time):.4f}")
        
        self.prediction_frame = PredictionFrame(self.model, self.model_df_raw, self.predict_callback, self)
        self.prediction_frame.grid(row = 0, column = 0, sticky = "wnse")
        
        self.loading_label_data.destroy()
        
        self.visualization_frame = VisualizationFrame(self.model, self.model_df_raw, self.data_tuple, self)
        self.visualization_frame.grid(row = 0, column = 1, sticky = "wnse")
        # Zet de cursor op normaal
        self.config(cursor="")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def load_data(self) -> None:
        print("loading model and model_df...")

        with open("./models/DecisionTreeRegressor.pkl", "rb") as file:
            self.model = pickle.load(file)

        self.model_df_raw = pd.read_pickle('data/model_df.pkl')

        print("model and model_df loaded\n")
        
        # ------------------------------------
        
        print("loading data...")
        with open("./data/df_gui.pkl", "rb") as file:
            self.data_tuple = pickle.load(file)
        print("data loaded\n")
        
    def predict_callback(self, X):
        self.visualization_frame.update_prediction(X)

    def on_closing(self):
        # Dit is gedaan, omdat je anders invalid command gedoe krijgt...
        self.withdraw()
        self.quit()

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
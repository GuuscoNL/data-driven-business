import customtkinter as ctk
from predictionFrame import PredictionFrame
from visualization import VisualizationFrame
import pickle
import pandas as pd

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1400

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
        
        self.load_data()
        self.prediction_frame = PredictionFrame(self.model, self.model_df_raw, self.predict_callback, self)
        self.prediction_frame.grid(row = 0, column = 0, sticky = "wnse")
                
        self.visualization_frame = VisualizationFrame(self.model, self.model_df_raw, self)
        self.visualization_frame.grid(row = 0, column = 1, sticky = "wnse")
        self.update()
        self.visualization_frame.init()
        # Zet de cursor op normaal
        self.config(cursor="")
        self.update()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    
    def load_data(self) -> None:
        """Laad het model en de kolommen die zijn gebruikt tijdens het fitten van het model.
        """
        # laad het model
        with open("./models/DecisionTreeRegressor.pkl", "rb") as file:
            self.model = pickle.load(file)
        
        # Laad het model dat is gebruikt tijdens het fitten van het model
        self.model_df_raw = pd.read_csv("data/model_df.csv", index_col=0)
        
    def predict_callback(self, X):
        print("Predicting...")
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
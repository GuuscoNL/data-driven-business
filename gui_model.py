import pandas as pd
import pickle
import time
import sys
import threading

# chatGPT :D
class CustomSpinner:
    def __init__(self):
        self.chars = ['-', '\\', '|', '/']
        self.is_running = False

    def start(self, duration=10):
        self.is_running = True
        self.spinner_thread = threading.Thread(target=self._spin, args=(duration,))
        self.spinner_thread.start()

    def stop(self):
        self.is_running = False

    def _spin(self, duration):
        start_time = time.time()
        while self.is_running and (time.time() - start_time) < duration:
            for char in self.chars:
                sys.stdout.write(char)
                sys.stdout.flush()
                sys.stdout.write('\b')
                time.sleep(0.1)

if __name__ == '__main__':
    spinner = CustomSpinner()

    print("Loading data...")
    spinner.start()
    cols_to_use = [
        'stm_geo_mld',
        'stm_oorz_code',
        'stm_fh_ddt',
        'stm_fh_dd',
        'stm_fh_duur',
    ]

    df_gui = pd.read_csv("./data/sap_storing_data_hu_project.csv", engine="pyarrow", usecols=cols_to_use)
    
    total_data = len(df_gui)
    df_gui.dropna(subset=["stm_geo_mld", "stm_fh_ddt"], inplace=True)
    all_geo_codes = sorted(df_gui["stm_geo_mld"].unique().tolist())
    df_gui["stm_geo_mld"] = df_gui["stm_geo_mld"].astype(str).replace(".0", "", regex=True)
    
    # make sure the date columns are datetime
    df_gui['stm_fh_ddt'] = pd.to_datetime(df_gui['stm_fh_ddt'], format='%d/%m/%Y %H:%M:%S', errors='coerce')

    result = (total_data, all_geo_codes, df_gui)
    with open("./data/df_gui.pkl", "wb") as file:
        pickle.dump(result, file)
    spinner.stop()
    spinner.spinner_thread.join()

    print("Data processed and saved in `./data/df_gui.pkl`")
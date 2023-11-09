# Prorail - NS
Het doel van dit project is om de functie herstel tijd te voorspellen voor Prorail. Zodat Prorail de herstel tijd kan gebruiken om NS planners te informeren over de verwachte herstel tijd van een storing. Dit kan de NS planners helpen om een betere inschatting te maken van de vertraging die een storing veroorzaakt. En zo de treinen beter te laten rijden.

# Data
De data die gebruikt wordt voor dit project is afkomstig van Prorail en is niet openbaar. Deze zou in de data folder moeten staan. De data is niet opgenomen in de repository omdat deze te groot is.

# Installatie
Om dit project te kunnen draaien moet je eerst de requirements installeren. Dit kan je doen door het volgende commando uit te voeren in de terminal:
```
pip install -r requirements.txt
```

# Startup
Zet de data in de ['data'](data) folder en noem het `sap_storing_data_hu_project.csv`. Daarna run je de volgende notebooks/scripts in de volgende volgorde:
- [`DataPrep.ipynb`](DataPrep.ipynb)
- [`dTreeReg.ipynb`](dTreeReg.ipynb)
- [`gui_model.ipynb`](gui_model.ipynb)

# Scripts
- [`app`](app)<br>
    In deze folder staat de code voor de app (dashboard). Deze kan worden gestart door `app.py` te runnen.

- [`TargetPrep.ipynb`](TargetPrep.ipynb)<br>
    In de notebook wordt de target variabele gemaakt en deze zal worden geroepen door de andere notebooks.

- [`DataPrep.ipynb`](DataPrep.ipynb)<br>
    In deze notebook wordt de data voorbereid voor het model. Hier worden de features gemaakt en de data wordt gesplitst in een train en test set. Deze notebook roept de target variabele aan uit de TargetPrep notebook. De data wordt opgeslagen in de [data](data) folder:
    - `model_df.pkl`
    - `test_df.pkl`
    - `train_df.pkl`
    - `feature_encoding.json` (wordt gebruikt voor het encoden van de features in de app)

- [`dTreeReg.ipynb`](dTreeReg.ipynb)<br>
    In deze notebook wordt het Decision Tree Regressor model getraind. Hier worden ook de ookhyperparameters getuned. Het model wordt opgeslagen in de [models](models) folder:
    - `DecisionTreeRegressor.pkl`

- [`ForestReg.ipynb`](ForestReg.ipynb)<br>
    In deze notebook wordt het Random Forest Regressor model getraind. Hier worden ook de ookhyperparameters getuned. Het model wordt opgeslagen in de [models](models) folder:
    - `RandomForestRegressor.pkl`

- [`LinearRegression.ipynb`](LinearRegression.ipynb)<br>
    In deze notebook wordt het Linear Regressor model getraind. Hier worden ook de ookhyperparameters getuned. Het model wordt opgeslagen in de [models](models) folder:
    - `LinearRegressor.pkl`

- [`baseline.py`](baseline.py)<br>
    In deze script wordt de baseline model berekend. Deze kan worden importeerd en berekend worden met behulp van de functie `calculate_baseline(df)`.

- [`gui.py`](gui.py)<br>
    In deze script wordt de model verwerkt voor de app. het bewerkte model wordt opgeslagen in de [data](data) folder:
    - `df_gui.pkl`

# LICENSE
Dit project is gelicenseerd onder de MIT License - zie de [LICENSE](LICENSE) file voor details.
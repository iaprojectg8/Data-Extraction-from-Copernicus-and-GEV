# Data extraction from Copernicus and GEV

## Environnement
To have the right environment in order to launch the application you need to follow these steps.
1. Ensure that you have python on your computer and that it is callable like this
```
>>> python --version
Python 3.11.4
```
Otherwise install it.

2. Ensure as well that you have pip that is pointing to your python version
```
>>> pip --version
C:\Users\FlorianBERGERE\AppData\Roaming\Python\Python311\site-packages\pip (python 3.11)
```
3. Create a python environment with this command
```
python -m venv appenv
```
4. Activate it:
```
.\appenv\Scripts\activate
```
5. Finally install all the packages
```
python -m pip install -r requirements.txt
```

## Start the App
As soon that you have done this you can start the App
```
streamlit run .\app.py    
```


## What you should know
The data extraction is very long, to give you an idea, for one year extraction of whatever climate variable, it takes about 20 minutes to extract.
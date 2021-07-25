# Freestyle Android LibreLink Data Extractor
This is a simple python 2.7 script for pulling data from an Android phone running LibreLink (US version) for Freestyle Libre sensor to CSV files on your PC/Mac (only tested on Mac). LibraLink stores data in SQL database files.  The script downloads the data from the phone, extracts the data, reads the SQL database for `historicReadings`, `notes`, and then merges them into a single CSV sorted by timestampUTC.

1. Install Android Debugger (ADB) by [Installing Android Studio](https://developer.android.com/studio)
2. Open a terminal, run `python extract.py`
3. Open the created `merged.csv` file in your favorite data analysis/visualization tool

![chart](https://github.com/jcl5m1/freestyle_libre_extractor/blob/main/chart.jpg?raw=true)

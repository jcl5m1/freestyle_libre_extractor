# Freestyle LibreLink Android Data Extractor/Exporter
This is a simple python 2.7 script for pulling data from an Android phone running LibreLink (US version) for Freestyle Libre sensor to CSV files on your PC/Mac (only tested on Mac).  It does not require a rooted Android phone. LibraLink stores data in SQL database files.  The script downloads the data from the phone, extracts the data, reads the SQL database for `historicReadings`, `notes`, and then merges them into a single CSV sorted by timestampUTC.

1. Install Android Debugger (ADB) by [Installing Android Studio](https://developer.android.com/studio)
2. Put your [Android phone into developer mode](https://www.google.com/search?q=how+to+turn+on+developer+mode+in+android), and connect to your PC/Mac via USB cable.
3. Open a terminal, and run `adb devices` to verify your computer can access the phone. You may need to confirm permission on your phone.
4. Run `python extract.py`.  You will have to approve the backup operation to allow the script to copy the database files from your phone.
5. You can now load the created `.csv` files in your favorite data analysis/visualization tool.  `merged.csv` is just the combined data.

![chart](https://github.com/jcl5m1/freestyle_libre_extractor/blob/main/chart.jpg?raw=true)

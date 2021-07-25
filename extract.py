import os
import sqlite3
import csv
import time

print("pulling data from phone")
# backup the freestyle libre data from app.  may need to change the suffix to match other countries
# based on https://gist.github.com/letsjump/71b2b62e809422e5e08862130fe444d7
os.system('adb backup -noapk com.freestylelibre.app.us')

print('extracting archive')
# format backup file to be proper tar archive
# https://stackoverflow.com/questions/18533567/how-to-extract-or-unpack-an-ab-file-android-backup-file
os.system("( printf \"\\x1f\\x8b\\x08\\x00\\x00\\x00\\x00\\x00\" ; tail -c +25 backup.ab ) |  tar xfvz -")

print('extracting data')
# load db in sql, and extract desired data
dbfile = "apps/com.freestylelibre.app.us/f/sas.db"
con = sqlite3.connect(dbfile)
cur = con.cursor()
data = cur.execute("SELECT glucoseValue, timestampLocal FROM realTimeReadings")

# create CSV using timestamp
file =  str(int(time.time()))+".csv"
with open(file, 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(['glucoseValue', 'timestampLocal'])
    writer.writerows(data)

con.close()

print("Cleanup")
os.system('rm backup.ab')
os.system('rm -rf apps')

print("Saved to " + file)

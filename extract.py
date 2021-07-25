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
def extract_to_csv(dbfile, tablename):
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    data = cur.execute("SELECT * FROM " + tablename)
    colnames = list(map(lambda x: x[0], cur.description))

    # create CSV using timestamp
    ts = str(int(time.time()))
    file = ts + '_' + tablename + ".csv"
    with open(file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(colnames)
        writer.writerows(data)
    con.close()
    return file

# load historical readings db in sql, and extract desired data
dbfile = "apps/com.freestylelibre.app.us/f/sas.db"
readingsFile = extract_to_csv(dbfile, 'historicReadings')
print("Saved to " + readingsFile)
dbfile = "apps/com.freestylelibre.app.us/f/apollo.db"
notesFile = extract_to_csv(dbfile, 'notes')
print("Saved to " + notesFile)

# merge CSVs using timestampUTC
def load_csv_as_dict(file):
    columns = []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if columns:
                for i, value in enumerate(row):
                    columns[i].append(value)
            else:
                # first row
                columns = [[value] for value in row]
    # you now have a column-major 2D array of your file.
    as_dict = {c[0] : c[1:] for c in columns}
    return as_dict

# merge both in to a single csv file sharing only timestampUTC
notes_dict = load_csv_as_dict(notesFile)
readings_dict = load_csv_as_dict(readingsFile)
merged = []
for i in range(len(notes_dict['timestampUTC'])):
    row = {}
    for c in notes_dict.keys():
        row[c] = notes_dict[c][i]
    for c in readings_dict.keys():
        if 'timestampUTC' not in c:
            row[c] = ''
    merged.append(row)

for i in range(len(readings_dict['timestampUTC'])):
    row = {}
    for c in readings_dict.keys():
        row[c] = readings_dict[c][i]
    for c in notes_dict.keys():
        if 'timestampUTC' not in c:
            row[c] = ''
    merged.append(row)

merged.sort(key=lambda x: x['timestampUTC'])

ts = str(int(time.time()))
file = ts + "_merged.csv"
with open(file, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(merged[0].keys())
    for row in merged:
        writer.writerow(row.values())

print("Cleanup")
os.system('rm backup.ab')
os.system('rm -rf apps')

print("Saved to " + file)

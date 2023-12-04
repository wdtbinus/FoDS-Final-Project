"""
Program reads charts CSV and outputs the top 100 charting artists.
"""

import csv
from datetime import date


def min_date(date_1, date_2):
    if date_1 < date_2:
        return date_1
    else:
        return date_2

def max_date(date_1, date_2):
    if date_1 > date_2:
        return date_1
    else:
        return date_2

def position_to_score(position):
    return 101 - int(position)

def time_delta(min_date, max_date):
    return date.fromisoformat(max_date) - date.fromisoformat(min_date)

linecount = 0
artists = {}
header = ["date","rank","song","artist","last-week","peak-rank","weeks-on-board"]
with open('charts.csv', newline='') as chartfile:
    file_reader = csv.reader(chartfile)
    for row in file_reader:
        linecount += 1
        rowdict = {header[i]: row[i] for i in range(0, len(header))}
        if rowdict['rank'] == 'rank':
            continue
        if rowdict["artist"] in artists:
            artist = artists[rowdict['artist']]
            artist['score'] += position_to_score(rowdict['rank'])
            artist['min_date'] = min_date(artist['min_date'], rowdict['date'])
            artist['max_date'] = max_date(artist['max_date'], rowdict['date'])
        else:
            artists[rowdict['artist']] = {
                "artist": rowdict['artist'],
                "score": position_to_score(rowdict['rank']),
                "min_date": rowdict['date'],
                "max_date": rowdict['date'],
            }

print("Input file had " + str(linecount) + " lines")
artist_out = [artists[key] for key in artists]
artist_out.sort(key=lambda a: a['score'], reverse=True)
print("Here are the top 100 artists on Billboard:")
for x in range(0, 100):
    print(artist_out[x])

for a in artist_out:
    a['career_length (days)'] = time_delta(a['min_date'], a['max_date']).days

cols = ['rank', 'artist', 'min_date', 'max_date', 'score', 'career_length (days)']

with open('top_100_artists.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(cols)
    for x in range(0, 100):
        artist = artist_out[x]
        record = [artist[c] for c in cols if c != 'rank']
        record.insert(0, x + 1)
        csvwriter.writerow(record)
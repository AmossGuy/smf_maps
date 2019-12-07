#!/usr/bin/env python3

csvpath = myfolder / Path(input("Path to CSV file TO WRITE (relative to the directory this script is in): "))

with open(csvpath, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for i in level:
        writer.writerow(i)

#It is for getting a list of Uniprot IDs and then Downloading them all from UniProt DB
import os
import glob
import sys
from math import ceil
NumOfBatch  = int(sys.argv[1])

PfamCordsPath = "./tmp/PfamCordsOnSeedsOneLineFormatAFadj.tsv"
NoOfStructs = sum(1 for _ in open(PfamCordsPath))

file = open(PfamCordsPath)
out  = open("./tmp/B1_Cords.txt", 'w')


batch = ceil(NoOfStructs/NumOfBatch)

counter = 0
for line in file:
    out.write(line)
    counter += 1
    if counter%batch==0:
        out.close()
        batchNum = counter//batch + 1
        out = open(f"./tmp/B{batchNum}_Cords.txt", 'w')
#out.write("  .\n")
out.close()
file.close()

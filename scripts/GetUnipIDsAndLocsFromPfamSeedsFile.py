#This is for getting the UnipID and locations of domains
#Of pfam seeds. It will also store their sequence

import os
import sys
tmp = "./tmp"
#downloading Pfam Seeds file

os.system(f"wget -P {tmp} https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.seed.gz")
os.system(f"gunzip {tmp}/Pfam-A.seed.gz")



file = open(f"{tmp}/Pfam-A.seed",encoding="latin-1")

outputFile = open(f"{tmp}/PfamSeedsTwoIDsAndLocs.tsv", 'w')

PfamSeedsFasta = open(f"{tmp}/PfamSeeds.fasta",'w')

JustIDs = open(f"{tmp}/JustIDsOfSeeds.csv",'w')
PF = ""

IDsList = []

for line in file:
    if line.startswith("#=GF AC"):
        PF = line.strip().split()[-1].split(".")[0]
        NameDict = {}
    elif line.startswith("#=GS "):
        if line.split()[2]=="AC":
            UnipID = line.strip().split()[-1].split(".")[0]
            IDsList.append(UnipID)
            Start, End = line.split()[1].split("/")[1].split("-")
            LongName = line.split()[1]
            NewDesig = "_".join([UnipID, Start, End, PF])
            NameDict[LongName] = NewDesig
            outputFile.write("\t".join([UnipID, Start, End, PF, LongName]) + "\n")
    elif line[0].isalnum():
        LongName = line.split()[0]
        Seq = line.split()[1]
        
        PfamSeedsFasta.write(">" + NameDict[LongName] + "\n" + Seq.strip().replace(".",'').upper() + "\n")

JustIDs.write("\n".join(sorted(list(set(IDsList)))))
JustIDs.close()
PfamSeedsFasta.close()
outputFile.close()

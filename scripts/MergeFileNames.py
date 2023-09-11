import os
import glob
import sys
from math import ceil
tmp="./tmp"

def MergeFiles(filename1, filename2, outputname):
    with open(filename1, "r") as file1, open(filename2, "r") as file2, open(outputname, "w") as merged_file:
        line1 = file1.readline()
        line2 = file2.readline()
        while line1 and line2:
            if line1 < line2:
                merged_file.write(line1.strip() + "\n")
                line1 = file1.readline()
            else:
                merged_file.write(line2.strip() + "\n")
                line2 = file2.readline()
        while line1:
            merged_file.write(line1.strip() + "\n")
            line1 = file1.readline()
        while line2:
            merged_file.write(line2.strip() + "\n")
            line2 = file2.readline()

files = sorted(glob.glob( tmp +"/part-???.csv"))
level = 0
while len(files)!= 1:
    NumOfBatches = ceil(len(files)/2)
    NewNames = []
    for i in range(NumOfBatches):
        files2merge = files[2*i:2*i+2]
        outfileName = tmp +f"/merged_level_{level}_num_{i}.csv"
        if len(files2merge)==1:
            os.system(f"cp {files2merge[0]} {outfileName}")
        else:
            MergeFiles(*files2merge, outfileName)
        NewNames.append(outfileName)
    files = NewNames
    level += 1
os.system(f"mv {files[0]} {tmp}/AllAF_IDs.csv")

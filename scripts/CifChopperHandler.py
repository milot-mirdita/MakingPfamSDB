import sys
import tarfile
import io
from io import StringIO
from CifChopper import CifChopper
import glob
import gzip
import os


tarFileName = sys.argv[1]
LocationFileName = sys.argv[2]

tarOut = tarfile.TarFile(tarFileName.replace(".tar", "_chopped.tar"),"w")

tfile = tarfile.open(tarFileName, 'r|')
LocationFile = open(LocationFileName)
for t in tfile:
    gzFile = tfile.extractfile(t)
    f = gzip.open(gzFile, 'rt')
    UnipID = t.get_info()['name'].replace(".cif.gz", '')  #####adjust it
    fileLines = f.read().split("\n")
    #print(type(fileLines[0]))
    Locations = LocationFile.readline()
    parts = Locations.strip().split("\t")
    if len(parts)==1:
        continue
    parts = [parts[0]] + parts[1].split(",")
    if parts[0] !=  UnipID:
        os.system("touch error in B${SLURM_ARRAY_TASK_ID}" + parts[0])
        os.system("echo " + UnipID)
        exit()
    NumOfLos = (len(parts) - 1)//3
    for i in range(NumOfLos):
        start = int(parts[1+ 3*i])
        end = int(parts[2 + 3*i])
        pf = parts[3 + 3*i]
        try:
            ChoppedText = CifChopper(fileLines, start, end) #.encode("ASCII")             
        except:
            print(UnipID)
        NewName = UnipID + "_" +str(start) + "_" + str(end) + "_" + pf + ".pdb.gz"
        #Here I must make some changes so that the chopped region would be stored as a gzip file
        with gzip.open(NewName, 'wt') as outGzippedFile:
            outGzippedFile.write(ChoppedText)
        tarOut.add(NewName)
        os.remove(NewName)

tarOut.close()
tfile.close()
LocationFile.close()

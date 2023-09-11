import os
import glob
import sys
from math import ceil
tmp="./tmp"
from ConcatTars import ConcatTars

FileNum = len(glob.glob("../structures/B*.tar"))
files = [f"../structures/B{i}.tar" for i in range(1,FileNum+1)]
outputName = "../structures/Pfam_FL.tar"

ConcatTars(files, outputName)




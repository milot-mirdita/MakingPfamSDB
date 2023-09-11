import glob
import sys
tmp = "./tmp"
filenames = sorted(glob.glob(f"{tmp}/*_cif-part-*.csv"))

for filename in filenames:
    file = open(filename)
    ofile = open(filename.replace("manifest-model_v4_cif-",''),'w')
    IDs = []
    for line in file:
        IDs.append(line.split("-")[1])
    IDs = sorted(IDs)
    ofile.write("\n".join(IDs))
    ofile.close()

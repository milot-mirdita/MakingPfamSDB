import re
import sys
import tarfile
import os
import gzip


tarFileName = sys.argv[1]
tmp = "../scripts/tmp"
fastaFileName = os.path.basename(tarFileName).replace(".tar", ".fasta")
outf = open(f"{tmp}/{fastaFileName}", 'w')

tfile = tarfile.open(tarFileName, 'r|')

for t in tfile:
    gzFile = tfile.extractfile(t)
    f = gzip.open(gzFile, 'rt')
    UnipID = t.get_info()['name'].replace(".cif.gz", '')
    content = f.read()
    pattern = re.compile(r'_entity_poly\.pdbx_seq_one_letter_code(.*?)_entity_poly\.pdbx_seq_one_letter_code_can', re.DOTALL)
    match = pattern.search(content)
    sequence = match.group(1)
    sequence = "".join(sequence.split()).strip(";")
    outf.write(f">{UnipID}\n{sequence}\n")

tfile.close()


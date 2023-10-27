#!/usr/bin/env python3
# Get the id, locations and sequence of domains of pfam seeds
import sys

tmp_dir = "."
sys.stdin.reconfigure(encoding='latin-1')
input_file = sys.stdin

ids_list = []

with open(f"{tmp_dir}/pfam_seeds_two_ids_and_locs.tsv", 'w') as output_file, \
     open(f"{tmp_dir}/pfam_seeds.fasta", 'w') as pfam_seeds_fasta, \
     open(f"{tmp_dir}/just_ids_of_seeds.csv", 'w') as just_ids:
    
    name_dict = {}
    for line in input_file:
        if line.startswith("#=GF AC"):
            pf_id = line.strip().split()[-1].split(".")[0]
            name_dict = {}
        elif line.startswith("#=GS "):
            if line.split()[2] == "AC":
                unip_id = line.strip().split()[-1].split(".")[0]
                ids_list.append(unip_id)
                start, end = line.split()[1].split("/")[1].split("-")
                long_name = line.split()[1]
                new_desig = "_".join([unip_id, start, end, pf_id])
                name_dict[long_name] = new_desig
                output_file.write("\t".join([unip_id, start, end, pf_id, long_name]) + "\n")
        elif line[0].isalnum():
            long_name = line.split()[0]
            seq = line.split()[1]
            pfam_seeds_fasta.write(">" + name_dict[long_name] + "\n" + seq.strip().replace('.', '').upper() + "\n")

    just_ids.write("\n".join(sorted(list(set(ids_list)))))


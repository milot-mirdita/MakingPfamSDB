#!/usr/bin/env python3

import pandas as pd

tmp_dir = "."

pf_cords = pd.read_csv(f"{tmp_dir}/pfam_seeds_two_ids_and_locs.tsv", sep="\t", header=None)

with open(f"{tmp_dir}/seed_af_intersect.tsv", 'r') as file:
    pfam_seeds_in_af = [line.strip() for line in file.readlines()]

pf_cords = pf_cords[pf_cords[0].isin(pfam_seeds_in_af)]
pf_cords.sort_values(by=0, inplace=True)
pf_cords = pf_cords[[0, 1, 2, 3]]
pf_cords.reset_index(drop=True, inplace=True)
pf_cords[3] = pf_cords[1].astype(str) + "," + pf_cords[2].astype(str) + "," + pf_cords[3]
pf_cords = pf_cords[[0, 3]]
pf_cords_concat = pf_cords.groupby(0).agg({3: lambda x: ','.join(x)}).reset_index()
pf_cords_concat.to_csv(f"{tmp_dir}/pfam_cords_on_seeds_one_line_format.tsv", sep="\t", index=None, header=None)


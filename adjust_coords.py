#!/usr/bin/env python3

def extract_accession(header):
    return header.split("-")[1]

def extract_identity(header):
    return header

def return_fasta_dict(file_path, header_transform):
    with open(file_path, 'r') as file:
        lines = file.read().strip().split("\n")
    seq_dict = {header_transform(lines[i].strip(">")): lines[i + 1].upper() for i in range(0, len(lines), 2)}
    return seq_dict

tmp_dir = "."

pfam_seeds = return_fasta_dict(f"{tmp_dir}/pfam_seeds.fasta", extract_identity)
pfam_seeds_fl_af = return_fasta_dict(f"{tmp_dir}/flpss_af.fasta", extract_accession)

pfam_seeds_af = {}

with open(f"{tmp_dir}/pfam_cords_on_seeds_one_line_format.tsv", 'r') as pfam_cords:
    for line in pfam_cords:
        seq_id, cords_and_pfs = line.strip().split("\t")
        cords_and_pfs = cords_and_pfs.split(",")
        for i in range(0, len(cords_and_pfs), 3):
            start, end, pf = int(cords_and_pfs[i]), int(cords_and_pfs[i + 1]), cords_and_pfs[i + 2]
            key = f"{seq_id}_{start}_{end}_{pf}"
            pfam_seeds_af[key] = pfam_seeds_fl_af[seq_id][start-1:end]

differing_seqs = [prot for prot, seq in pfam_seeds_af.items() if seq != pfam_seeds.get(prot, '')]
print(f"The number of different sequences is {len(differing_seqs)}")

with open(f"{tmp_dir}/pfam_cords_on_seeds_one_line_format.tsv", 'r') as pfam_cords, \
     open(f"{tmp_dir}/pfam_cords_on_seeds_one_line_format_afadj.tsv", 'w') as pfam_corrected_cords, \
     open(f"{tmp_dir}/pfam_discarded_cords.tsv", 'w') as discarded_file:

    for line in pfam_cords:
        seq_id, cords_and_pfs = line.strip().split("\t")
        cords_and_pfs = cords_and_pfs.split(",")
        new_set = []
        discarded_set = []

        for i in range(0, len(cords_and_pfs), 3):
            concat_name = f"{seq_id}_{cords_and_pfs[i]}_{cords_and_pfs[i+1]}_{cords_and_pfs[i+2]}"
            if concat_name not in differing_seqs:
                new_set.extend(cords_and_pfs[i:i+3])
            else:
                discarded_set.extend(cords_and_pfs[i:i+3])

        if new_set:
            pfam_corrected_cords.write(f"{seq_id}\t{','.join(new_set)}\n")

        if discarded_set:
            discarded_file.write(f"{seq_id}\t{','.join(discarded_set)}\n")

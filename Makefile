FOLDSEEK=/home/mmirdit/repositories/foldseek/build/src/foldseek
AFDB=/fast/databases/foldseek/afdb/afdb

.PHONY: retained_files ALL

ALL: pfam_fscut.dbtype

Pfam-A.seed.gz:
	aria2c -x16 -s32 https://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam35.0/Pfam-A.seed.gz

pfam_seeds_two_ids_and_locs.tsv pfam_seeds.fasta just_ids_of_seeds.csv: Pfam-A.seed.gz
	zcat Pfam-A.seed.gz | ./process_seeds.py

all_af_ids.tsv: $(AFDB).lookup
	cut -d'-' -f2 $(AFDB).lookup > all_af_ids.tsv

seed_af_intersect.tsv: just_ids_of_seeds.csv all_af_ids.tsv
	awk 'NR == FNR { f[$$1] = 1; next; } $$1 in f { print; }' just_ids_of_seeds.csv all_af_ids.tsv > seed_af_intersect.tsv

seed_af_keys.tsv: just_ids_of_seeds.csv $(AFDB).lookup
	awk 'NR == FNR { f["AF-"$$1"-F1-model_v4"] = 1; next; } $$2 in f { print $$1; }' just_ids_of_seeds.csv $(AFDB).lookup > seed_af_keys.tsv

pfam_seed.dbtype: seed_af_keys.tsv
	$(FOLDSEEK) createsubdb seed_af_keys.tsv $(AFDB) pfam_seed

flpss_af.fasta: pfam_seed.dbtype
	$(FOLDSEEK) convert2fasta pfam_seed flpss_af.fasta

pfam_seed_ss.dbtype: seed_af_keys.tsv
	$(FOLDSEEK) createsubdb seed_af_keys.tsv $(AFDB)_ss pfam_seed_ss

flpss_af_ss.fasta: pfam_seed_ss.dbtype
	$(FOLDSEEK) convert2fasta pfam_seed_ss flpss_af_ss.fasta

pfam_seed_ca.dbtype: seed_af_keys.tsv
	$(FOLDSEEK) createsubdb seed_af_keys.tsv $(AFDB)_ca pfam_seed_ca

flpss_af_ca.fasta: pfam_seed_ca.dbtype pfam_seed.dbtype pfam_seed_ss.dbtype
	$(FOLDSEEK) compressca pfam_seed pfam_seed_ca_f64 --coord-store-mode 3
	$(FOLDSEEK) lndb pfam_seed_h pfam_seed_ca_f64_h
	$(FOLDSEEK) convert2fasta pfam_seed_ca_f64 flpss_af_ca.fasta
	$(FOLDSEEK) rmdb pfam_seed_ca_f64
	$(FOLDSEEK) rmdb pfam_seed_ca_f64_h

pfam_cords_on_seeds_one_line_format.tsv: pfam_seeds_two_ids_and_locs.tsv seed_af_intersect.tsv
	./extract_coords.py

pfam_cords_on_seeds_one_line_format_afadj.tsv pfam_discarded_cords.tsv: pfam_seeds.fasta flpss_af.fasta pfam_cords_on_seeds_one_line_format.tsv
	./adjust_coords.py

retained_files: flpss_af.fasta flpss_af_ss.fasta flpss_af_ca.fasta pfam_cords_on_seeds_one_line_format_afadj.tsv
	./cut_fasta.py

retained_flpss_af.tsv retained_flpss_af_ss.tsv retained_flpss_af_ca.tsv retained_flpss_h.tsv: retained_files

pfam_fscut.dbtype: retained_flpss_af.tsv retained_flpss_af_ss.tsv retained_flpss_af_ca.tsv retained_flpss_h.tsv
	$(FOLDSEEK) tsv2db retained_flpss_af.tsv pfam_fscut --output-dbtype 0
	$(FOLDSEEK) tsv2db retained_flpss_af_ss.tsv pfam_fscut_ss --output-dbtype 0
	$(FOLDSEEK) tsv2db retained_flpss_af_h.tsv pfam_fscut_h --output-dbtype 12
	$(FOLDSEEK) tsv2db retained_flpss_af_ca.tsv pfam_fscut_ca --output-dbtype 12
	$(FOLDSEEK) compressca pfam_fscut pfam_fscut_ca2 --coord-store-mode 2
	$(FOLDSEEK) rmdb pfam_fscut_ca
	$(FOLDSEEK) mvdb pfam_fscut_ca2 pfam_fscut_ca


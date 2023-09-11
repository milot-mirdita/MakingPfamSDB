#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1
#SBATCH --time=00:5:00           # time (DD-HH:MM)
#SBATCH --output=logs/slurm-ExtractFasta-%j.out

set -e


batch=B$SLURM_ARRAY_TASK_ID
tmp=$1


python ExtractFastaFromTar.py ../structures/${batch}.tar $tmp
cat ${tmp}/B*.fasta > ${tmp}/FLPSS_AF.fasta

rm ${tmp}/B*.fasta

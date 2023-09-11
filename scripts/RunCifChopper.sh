#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1
#SBATCH --time=6:00:00           # time (DD-HH:MM)
#SBATCH --output=logs/slurm-ChopStructs-%j.out

set -e

batch=B$SLURM_ARRAY_TASK_ID

python CifChopperHandler.py ../structures/${batch}.tar ./tmp/${batch}_Cords.txt

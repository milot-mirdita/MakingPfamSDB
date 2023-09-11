#!/bin/bash

set -e
mkdir -p logs
mkdir -p tmp

bash GetAllUnipStructsInAlphaDB.sh

python GetUnipIDsAndLocsFromPfamSeedsFile.py

python FindAF_SeedsOverlap.py

python GetOneLineDescOfPfamSeeds.py

python ConvertUnipID2LinkAndGetReadyForDownloading.py $1

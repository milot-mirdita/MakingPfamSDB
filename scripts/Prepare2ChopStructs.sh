set -e
cat ./tmp/B*.fasta > ./tmp/FLPSS_AF.fasta
rm ./tmp/B*.fasta
python FindDiffBetAFdbAndPfamSeqAndAdjustCordsFile.py
NumOfJobs=$(ls ../structures/B*.tar | wc -l)
python SplitPfamCordsFiles.py $NumOfJobs

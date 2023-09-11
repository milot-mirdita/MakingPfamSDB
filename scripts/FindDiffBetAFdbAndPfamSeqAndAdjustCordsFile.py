# To run this script, you must have extracted the amino acid sequence of the Pfam
# Seeds, and then chop the regions where Pfam were predicted.



def ReturnFastaDict(fileAdd):
    file = open(fileAdd)
    lines = file.read().strip().split("\n")
    NumOfSeq = len(lines)//2
    SeqDict = {}
    for i in range(NumOfSeq):
        SeqDict[lines[2*i].strip(">")] = lines[2*i +1].upper()
    return SeqDict

PfamSeeds = ReturnFastaDict("./tmp/PfamSeeds.fasta")
PfamSeedsFL_AF = ReturnFastaDict("./tmp/FLPSS_AF.fasta")

PfamSeedsAF = {}

PfamCords = open("./tmp/PfamCordsOnSeedsOneLineFormat.tsv")
for line in PfamCords:
    SeqID = line.split("\t")[0]
    CordsAndPFs = line.strip().split("\t")[1].split(",")
    NumOfParts = len(CordsAndPFs)//3
    for i in range(NumOfParts):
        start = int(CordsAndPFs[i*3])
        end = int(CordsAndPFs[i*3 +1])
        PF = CordsAndPFs[i*3 + 2]
        PfamSeedsAF[SeqID + "_" + str(start) + "_" + str(end) + "_" + PF] = PfamSeedsFL_AF[SeqID][start-1:end]
PfamCords.close()


DifferingSeqs = []
for Prot in PfamSeedsAF.keys():
    if PfamSeedsAF[Prot]!= PfamSeeds[Prot]:
        DifferingSeqs.append(Prot)
print("The number of different sequences is " + str(len(DifferingSeqs)))

PfamCords = open("./tmp/PfamCordsOnSeedsOneLineFormat.tsv")
PfamCorrectedCords = open("./tmp/PfamCordsOnSeedsOneLineFormatAFadj.tsv",'w')
for line in PfamCords:
    SeqID = line.split("\t")[0]
    CordsAndPFs = line.strip().split("\t")[1].split(",")
    NumOfParts = len(CordsAndPFs)//3
    NewSet = []
    for i in range(NumOfParts):
        ConCatName = "_".join([SeqID,CordsAndPFs[i*3],CordsAndPFs[i*3+1], CordsAndPFs[i*3+2] ])
        if ConCatName not in DifferingSeqs:
            NewSet = NewSet + [CordsAndPFs[i*3],CordsAndPFs[i*3+1], CordsAndPFs[i*3+2]]
    PfamCorrectedCords.write(SeqID + "\t" + ",".join(NewSet) + "\n")
    #PfamSeedsAF[SeqID + "_" + str(start) + "_" + str(end) + "_" + PF] = PfamSeedsFL_AF[SeqID][start-1:end]
PfamCorrectedCords.close()
PfamCords.close()

# convert 3 maf files to multi sample vcf
# start counting at 1
# chrom:5, start:6, end:7, SNP:10, Ref:11, Alt1:12, Alt2:13, dbSNP:14, Tumor_Sample_Barcode:16

def writeVcf(outputVcf, vcfOrder, dictVcf):
    pass

def main(inputMaf, outputVcf):
    firstLine  = '##fileformat=VCFv4.0\n'
    secondLine = '#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT'
    samplesArray = [] 
    arrayOrder   = [] # chrom,pos
    variantArray = [] # [id, ref, alt, qual, filter, info, format, S1, S2]
    dictVcf      = {} # chrom,pos = [id, ref, alt, qual, filter, info, format, S1, S2]
    dictAlt      = {} # chrom,pos = [alt1, alt2]
    outputVcf.write(firstLine)
    outputVcf.write(secondLine)
    inputFile = open(inputMaf, 'r')
    count = 0
    for row in inputFile:
        if row.startswith('#') or row.startswith('Hugo_Symbol'):
            continue
        count += 1
        cols = row.split('\t')

        # samples array to build the FORMAT column with the genotypes
        if cols[15] not in samplesArray:
            # complemente all other variants with a reference genotype
            for key,value in dictAlt.items():
                if value == None:
                    value = []
                    dictAlt[key] = []
                for i in range(len(value),len(samplesArray)):
                    dictAlt[key] = dictAlt[key].append('0/0')
            samplesArray.append(cols[15])

        # to keep track if we already saw this position
        if cols[4]+','+cols[5] not in arrayOrder:
            arrayOrder.append(cols[4]+','+cols[5])
            variantArray = [cols[4],cols[5],cols[13],cols[10],cols[11],'.','.','.','GT',cols[15]]
            dictVcf[cols[4]+','+cols[5]] = variantArray
            tmpAlt = []
            for iAlt in cols[11].split(','):
                dictAlt[cols[4]+','+cols[5]] = tmpAlt.append(iAlt)
            dictAlt[cols[4]+','+cols[5]] = tmpAlt
    inputFile.close()
    print('rows:', inputMaf, count)

if __name__ == '__main__':
    kirp = 'maf/TCGA.KIRP.mutect.somatic.maf'
    kirc = 'maf/TCGA.KIRC.mutect.somatic.maf'
    kich = 'maf/TCGA.KICH.mutect.somatic.maf'

    # convert maf to vcf
    outputKirp = open('maf_kirp.vcf', 'w')
    outputKirc = open('maf_kirc.vcf', 'w')
    outputKich = open('maf_kich.vcf', 'w')
    main(kirp, outputKirp)
    main(kirc, outputKirc)
    main(kich, outputKich)
    outputKirp.close()
    outputKirc.close()
    outputKich.close()
    ### TODO create tabix file after ###

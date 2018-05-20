# genotype clustering base on renal papillary cell carcinoma
# unsupervised clustering
# dimensionality reduction
# pip install --user pytabix

import shutil
import tempfile
import urllib.request

# our vcf or genotypes file
sampleFile="sample_file.txt"

# load data into pandas
import pandas as pd
anon = pd.read_table(sampleFile, sep = "\t", comment = "#", header = None, low_memory=False)
#print("The genotype datset has {} rows and {} columns.".format(anon.shape[0], anon.shape[1]))
#print(anon.head())
anon = anon.iloc[0:1000,:] # TODO REMOVE for testing with a small set

# rename columns
anon.columns = ["rsid", "chrom", "pos", "genotype"]
#print(anon.head())

# setting up tabix
import tabix
AAA_file = "AAA.low_coverage.genotypes.vcf.gz"
aaa = tabix.open(AAA_file)
rs3094315 = aaa.query("1", 742428, 742429)  # an iterator object
print(rs3094315.__next__())

# convert to vcf genomes format of 1/0 (instead of genotypes format)
def convert_anon_genotype(chrom, pos, genotype, vcf_tabix):
    site = vcf_tabix.query(chrom, pos - 1, pos)
    try:
        row = site.__next__() # this will throw an error (which is caught by 'except' on the next line) if the site we queried is not in the tabix file
    except StopIteration:
        return None # put None in the dataframe if we are missing this genotype in the Genome Datasets
    ref = row[3]
    alt = row[4]
    if genotype == ref+ref:
        return("0|0")
    elif (genotype == ref+alt) | (genotype == alt+ref):
        return("0|1")
    elif genotype == alt+alt:
        return("1|1")
    else: # missing genotype, or incorrect annotation, we assume ref/ref
        return("0|0")

# is this part of convertig to 1k genomes format??
genotypes_1kg_format = []
for chrom, pos, genotype in zip(anon['chrom'], anon['pos'], anon['genotype']):
    genotypes_1kg_format.append(convert_anon_genotype(str(chrom), pos, genotype, aaa))
anon['genotype_1kg_format'] = genotypes_1kg_format
print(anon.head())
print(anon.shape)


# Making a Featurespace from our Genotypes
# make a data frame with one row for each of the a samples
a_genotypes = pd.DataFrame({"sample": ["AAA" + str(i) for i in range(1, 60)], "population": "AAA"})
print(a_genotypes.head())

# extract genotype information for a set of sites
def extract_genotype(chrom, pos, vcf_tabix):
    site = vcf_tabix.query(chrom, pos - 1, pos)
    try:
        g = site.__next__()[9:]
    except StopIteration:
        return None # put None in the dataframe if we are missing this genotype in the Genome Datasets
    g = [i.split(":")[0] for i in g]  # if present in genomes datasets, get the genotypes
    return(g)

for rsid, chrom, pos in zip(anon['rsid'], anon['chrom'], anon['pos']):
    g = extract_genotype(str(chrom), pos, aaa)
    a_genotypes[rsid] = g

print("The dataframe including all of the samples from the a population has {} samples and {} genotypes.".format(a_genotypes.shape[0], a_genotypes.shape[1] - 2))

print(a_genotypes.iloc[0:10, 0:7])

# b dataset
BBB_file = "BBB.low_coverage.genotypes.vcf.gz"
bbb = tabix.open(BBB_file)

number_bbb_samples = len(bbb.query("1", 742428, 742429).__next__()[9:])

bbb_genotypes = pd.DataFrame({"sample": ["BBB" + str(i) for i in range(1, number_bbb_samples + 1)], "population": "BBB"})

# c dataset
CCC_file = "CCC.low_coverage.genotypes.vcf.gz"
ccc = tabix.open(CCC_file)

number_ccc_samples = len(ccc.query("1", 742428, 742429).__next__()[9:])

ccc_genotypes = pd.DataFrame({"sample": ["CCC" + str(i) for i in range(1, number_ccc_samples + 1)], "population": "CCC"})

for rsid, chrom, pos in zip(anon['rsid'], anon['chrom'], anon['pos']):
    a_genotypes[rsid] =  extract_genotype(str(chrom), pos, aaa)
    bbb_genotypes[rsid] =  extract_genotype(str(chrom), pos, bbb)
    ccc_genotypes[rsid] =  extract_genotype(str(chrom), pos, ccc)

genotypes = a_genotypes.copy()
genotypes = genotypes.append(bbb_genotypes, ignore_index=True)
genotypes = genotypes.append(ccc_genotypes, ignore_index=True)

print("Now the genotypes data frame has {} samples and {} genotypes".format(genotypes.shape[0], genotypes.shape[1]-2))
# Now the genotypes data frame has # samples and anon genotypes normal or reduced


### Unsupervised Clustering using Principal Component Analysis ###
from sklearn.decomposition import PCA
pca = PCA(n_components = 2)

genotypes_only = genotypes.copy().iloc[:, 2:]  # we make a copy here, otherwise pandas will gripe at us!
genotypes_only[genotypes_only == "1|1"] = 1
genotypes_only[genotypes_only == "0|1"] = 0.5
genotypes_only[genotypes_only == "0/1"] = 0.5
genotypes_only[genotypes_only == "1|0"] = 0.5
genotypes_only[genotypes_only == "0|0"] = 0.0

# remove variants with None
genotypes_only = genotypes_only.dropna(axis=1)

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
# %matplotlib inline  ### only for jupyter notebook

pca.fit(genotypes_only)
pc = pca.transform(genotypes_only)

plt.figure(figsize=(10,6))
plt.scatter(pc[:, 0], pc[:, 1])
plt.title('Unsupervised clustering of our SNPs')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()   ### TODO change this?
plt.savefig('1st.png')

# 
import numpy as np
plt.figure(figsize=(10,6))
for c, pop in zip("rby", ["AAA", "BBB", "CCC"]):
    plt.scatter(pc[np.where(genotypes['population'] == pop), 0], pc[np.where(genotypes['population'] == pop), 1], c = c, label = pop)
plt.title('Unsupervised clustering of our SNPs')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.legend(loc = 'upper left')
plt.show()   ### TODO change this?
plt.savefig('2nd.png')


# keep only the genotypes used in our PCA above
anon = anon.loc[anon['rsid'].isin(genotypes_only.columns.values), :]  # only keep the genotypes data where we have no missing data in our datasets

anon_genotypes = anon.copy()["genotype_1kg_format"]

anon_genotypes[anon_genotypes == "1|1"] = 1
anon_genotypes[anon_genotypes == "0|1"] = 0.5
anon_genotypes[anon_genotypes == "1|0"] = 0.5
anon_genotypes[anon_genotypes == "0|0"] = 0.0
#anon_genotypes[anon_genotypes == None] = 0.0
anon_genotypes = anon_genotypes.reshape(1,-1) # reshape, otherwise sci-kit learn will throw a deprecation warning

# assume any missing data in our genotype sample is ref/ref
#anon_genotypes[anon_genotypes is None] = "0|0"

anon_pca = pca.transform(anon_genotypes)  # cluster was fit on the genomes datasets and we use it to transform the anonymous genotypes

print(anon.head())


plt.figure(figsize=(10,6))

for c, pop in zip("rgb", ["AAA", "BBB", "CCC"]):
    plt.scatter(pc[np.where(genotypes['population'] == pop), 0], pc[np.where(genotypes['population'] == pop), 1], c = c, label = pop)

# take the code above and add in the anonymous sample

plt.scatter(anon_pca[0,0], anon_pca[0,1], c = "yellow", label = "Our genotype Sample", marker = (5,1,0), s = 200)

plt.title('Unsupervised clustering of our SNPs')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.legend(loc = 'upper left')
plt.show()   ### TODO change this?
plt.savefig('3rd.png')

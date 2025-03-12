import scanpy as sc
import pandas as pd
import numpy as np
import snapatac2 as snap

rna = sc.read_h5ad('/data/CARD_singlecell/Brain_atlas/SN_Multiome/atlas/03_filtered_anndata_rna.h5ad')

# Import sample metadata
samples = pd.read_csv('/data/CARD_singlecell/SN_atlas/input/SN_PD_DLB_samples.csv')
batches = samples['Use_batch'].tolist()
samples = samples['Sample'].tolist()

# Read list of atac data locations
atac_anndata = [f'/data/CARD_singlecell/Brain_atlas/SN_Multiome/batch{batches[i]}/Multiome/{samples[i]}-ARC/outs/atac_fragments.tsv.gz' for i in len()]

# Read in snapATAC2 datasets into a list of anndata objects in read only
adatas = snap.pp.import_fragments(
    [fl for fl in atac_anndata],
    chrom_sizes=snap.genome.hg38.chrom_sizes,
    min_num_fragments=500,
)

# Get the fragment distribution (for later QC)
_ = snap.pl.frag_size_distr(adatas, show=False)
# Get the transcription start sites 
snap.metrics.tsse(adatas, snap.genome.hg38)

atac = snap.AnnDataSet(
    adatas=[(name, adata) for (name, _), adata in zip(samples, adatas)],
    filename="/data/CARD_singlecell/Brain_atlas/SN_Multiome/atlas/03_filtered_anndata_atac.h5ad"
)

# Add the consolidated cell-barcode 'atlas_identifier'
rna_samples = rna.obs['sample'].to_list()
rna_barcodes = rna.obs['cell_barcode'].to_list()
# Initialize cell-barcode 
rna_cell_barcode = []
for i in range(rna.n_obs):
    rna_cell_barcode.append(rna_samples[i] + '-' + rna_barcodes[i])

# Save the identifier
rna.obs['atlas_identifier'] = rna_cell_barcode

# Create the atlas identifier from the adataset obs
atac_df = atac.obs
atac_df['atlas_identifier'] = atac_df['index'] + '_' + atac_df['sample']
atac.obs = atac_df

# Subset RNA and ATAC objects based on the overlap of values
rna = rna[rna.obs['atlas_identifier'].isin(atac.obs['atlas_identifier'])].copy()
atac = atac[atac.obs['atlas_identifier'].isin(rna.obs['atlas_identifier'])].copy()

# Add the RNA observation data to the ATAC data
atac_df = pd.merge(
    left=atac_df,
    right=rna_df,
    left_on='atlas_identifier',
    right_on='atlas_identifier')
atac.obs = atac_df

# Select variable features
snap.pp.select_features(atac, n_features=250000, n_jobs=60)

# Spectral MDS analysis
snap.tl.spectral(atac)

# Batch correction›
snap.pp.mnc_correct(atac, batch="Sample", key_added='X_spectral')

# Perform k-nearest neighbors
snap.pp.knn(atac)

# Cluster 
snap.tl.leiden(atac)

# Calculate umap
snap.tl.umap(atac)

rna_annot = pd.read_csv('/data/CARD_singlecell/SN_atlas/data/rna_cell_annot.csv')
atac.obs['cell_type'] = rna_annot['cell_type'].to_list()

# Call peaks
snap.tl.macs3(atac, groupby='cell_type', replicate='sample')

# Be kind, rewind
atac.close()
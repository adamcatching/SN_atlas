import numpy as np
import pandas as pd
from pycisTopic.pseudobulk_peak_calling import export_pseudobulk
import scanpy as sc
import os

# Read in rna observation data
rna = sc.read_h5ad('/data/CARD_singlecell/Brain_atlas/SN_Multiome/atlas/05_annotated_anndata_rna.h5ad')

cell_data = rna.obs
cell_data['barcode'] = [x.split('_')[0] for x in cell_data.index]
# Add the sample_id variable
cell_data['sample_id'] = cell_data['sample']
# Only get the control cell
control_cell_data = cell_data[cell_data['Primary Diagnosis'] == 'control']

chromsizes = pd.read_table(
    "http://hgdownload.cse.ucsc.edu/goldenPath/hg38/bigZips/hg38.chrom.sizes",
    header = None,
    names = ["Chromosome", "End"]
)
chromsizes.insert(1, "Start", 0)

samples = cell_data['sample'].to_list()
batches = cell_data['batch'].to_list()
fragment_files = [f'/data/CARD_singlecell/Brain_atlas/SN_Multiome/batch{batches[i]}/Multiome/{samples[i]}-ARC/outs/atac_fragments.tsv.gz' for i in range(len(cell_data))]
fragments_dict = dict(zip(samples, fragment_files))

bw_paths, bed_paths = export_pseudobulk(
    input_data = cell_data,
    variable = "cell_type",
    chromsizes = chromsizes,
    bed_path = "/data/CARD_singlecell/SN_atlas/data/pycisTopic/consensus_peak_calling/pseudobulk_bed_files/",
    bigwig_path = "/data/CARD_singlecell/SN_atlas/data/pycisTopic/consensus_peak_calling/pseudobulk_bw_files/",
    path_to_fragments = fragments_dict,
    n_cpu = 40,
    normalize_bigwig = True,
    temp_dir = "/data/catchingba/cistopic"
    )

with open(os.path.join(out_dir, "/data/CARD_singlecell/SN_atlas/data/pycisTopic/consensus_peak_calling/bw_paths.tsv"), "wt") as f:
    for v in bw_paths:
        _ = f.write(f"{v}\t{bw_paths[v]}\n")

with open(os.path.join(out_dir, "/data/CARD_singlecell/SN_atlas/data/pycisTopic/consensus_peak_calling/bed_paths.tsv"), "wt") as f:
    for v in bed_paths:
        _ = f.write(f"{v}\t{bed_paths[v]}\n")


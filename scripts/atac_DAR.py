import snapatac2 as snap
import anndata as ad
import scipy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scanpy as sc
import episcanpy as epi
import decoupler as dc

# Load in the celltype atac object
cell_type_atac = sc.read_h5ad(snakemake.input.atac_anndata)

control_name = 'control'
disease_name = disease

cell_type_atac.var['chr'] = [x.split(':')[0] for x in cell_type_atac.var_names]
cell_type_atac.var['start'] = [int(x.split(':')[1].split('-')[0]) for x in cell_type_atac.var_names]
cell_type_atac.var['end'] = [int(x.split(':')[1].split('-')[1]) for x in cell_type_atac.var_names]
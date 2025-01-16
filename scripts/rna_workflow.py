import scvi
import scanpy as sc
import torch
import pandas as pd
import scipy
import numpy as np

scvi.settings.seed = 0
torch.set_float32_matmul_precision('high')

adata = sc.read_h5ad('/data/CARD_singlecell/SN_atlas/data/atlas/03_filtered_anndata_rna.h5ad')

adata.layers['counts'] = scipy.sparse.csr_matrix(adata.layers['counts'].copy())

sc.pp.highly_variable_genes(
    adata, 
    n_top_genes=int(sys.argv[1]), 
    batch_key="sample")

scvi.model.SCVI.setup_anndata(
    adata[:, adata.var['highly_variable']], layer="counts", batch_key="sample")

model = scvi.model.SCVI(
    adata[:, adata.var['highly_variable']], 
    dispersion="gene-batch", 
    n_layers=2, 
    n_latent=30, 
    gene_likelihood="nb"
)

model.train(
    max_epochs=1000,
    accelerator='gpu',  
    early_stopping=True,
    early_stopping_patience=20
)

elbo = model.history['elbo_train']
elbo['elbo_validation'] = model.history['elbo_validation']

adata.obsm['X_scvi'] = model.get_latent_representation()
sc.pp.neighbors(adata, use_rep='X_scvi')
sc.tl.umap(adata, min_dist=0.3)
sc.tl.leiden(adata,  resolution=.5, key_added='leiden_05')

adata.write_h5ad(f'/data/CARD_singlecell/SN_atlas/data/atlas/04_modeled_anndata_{str(sys.argv[1])}_rna.h5ad', compression='gzip')
elbo.to_csv(f'/data/CARD_singlecell/SN_atlas/data/model_elbo/rna_{str(sys.argv[1])}_model_history.csv', index=False)
model.save('/data/CARD_singlecell/SN_atlas/data/models/rna/500/', overwrite=True)

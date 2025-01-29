import muon as mu

mdata = mu.MuData({"RNA": snakemake.input.merged_rna_anndata, "ATAC": snakemake.input.merged_atac_anndata})

mdata.write(snakefile.output.merged_multiome)
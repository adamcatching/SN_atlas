import numpy as np
import pandas as pd
from pycisTopic.iterative_peak_calling import get_consensus_peaks
from pycisTopic.pseudobulk_peak_calling import peak_calling
import scanpy as sc
import pickle 
import os

"""REPLACE PATH"""
bw_paths = {}
with open("/data/CARD_singlecell/SN_atlas/data/pycisTopic/10_samples/bw_paths.tsv") as f:
    for line in f:
        v, p = line.strip().split("\t")
        bw_paths.update({v: p})

bed_paths = {}
with open("/data/CARD_singlecell/SN_atlas/data/pycisTopic/10_samples/bed_paths.tsv") as f:
    for line in f:
        v, p = line.strip().split("\t")
        bed_paths.update({v: p})

macs_path = "macs2"

"""REPLACE DIRECTORY"""
os.makedirs("/data/CARD_singlecell/SN_atlas/data/pycisTopic/consensus_peak_calling/MACS", exist_ok = True)

narrow_peak_dict = peak_calling(
    macs_path = macs_path,
    bed_paths = bed_paths,
    outdir = "/data/CARD_singlecell/SN_atlas/data/pycisTopic/consensus_peak_calling/MACS",
    genome_size = 'hs',
    n_cpu = 32,
    input_format = 'BEDPE',
    shift = 73,
    ext_size = 146,
    keep_dup = 'all',
    q_value = 0.05,
    _temp_dir = '/data/catchingba/cistopic'
)

# Other param
peak_half_width=250
# Get consensus peaks
consensus_peaks = get_consensus_peaks(
    narrow_peaks_dict = narrow_peak_dict,
    peak_half_width = peak_half_width,
    chromsizes = chromsizes)

"""FIX OUT DIR"""
consensus_peaks.to_bed(
    path = "/data/CARD_singlecell/SN_atlas/data/pycisTopic/consensus_peak_calling/consensus_regions.bed",
    keep =True,
    compression = 'infer',
    chain = False)

# Save peaks as dictionary
with open("/data/CARD_singlecell/SN_atlas/data/pycisTopic/consensus_peak_calling/MACS/narrow_peaks_dict.pkl", 'wb') as f:
  pickle.dump(narrow_peak_dict, f)
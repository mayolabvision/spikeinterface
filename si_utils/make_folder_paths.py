from pathlib import Path
import os

def make_folder_paths(spikeglx_folder,IMEC):
    medicine_folder = Path(spikeglx_folder) / f"{Path(spikeglx_folder).name}_imec{IMEC}" / 'medicine'
    preprocess_folder = Path(spikeglx_folder) / f"{Path(spikeglx_folder).name}_imec{IMEC}" / 'preprocess'
    
    figs_folder = Path(spikeglx_folder) / "figs" / "preprocess"
    os.makedirs(figs_folder, exist_ok=True)

    return medicine_folder, preprocess_folder, figs_folder

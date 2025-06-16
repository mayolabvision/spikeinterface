import numpy as np
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import time
import shutil

import spikeinterface.full as si
from spikeinterface.sortingcomponents.motion import correct_motion_on_peaks, interpolate_motion
from spikeinterface.sorters import run_sorter

from si_utils import *

#------------------------------------------------------------------------------------------------------------#
def si_h2p(spikeglx_folder, IMEC=0, drift_preset="dredge", plot_figs=False):

    t = time.time()

    global_job_kwargs = dict(n_jobs=40, chunk_duration='1s', progress_bar=True)
    si.set_global_job_kwargs(**global_job_kwargs)
    
    print("Step 1: Setting up folders and reading raw recording...")
    motion_folder, preprocess_folder, figs_folder = make_folder_paths(spikeglx_folder, IMEC)
    print(preprocess_folder)

    if os.path.isdir(preprocess_folder):
        print(f"The folder '{preprocess_folder}' already exists.")
        REC_CORRECTED = si.load(preprocess_folder)
        REC_CORRECTED

    else:
        stream_names, stream_ids = si.get_neo_streams('spikeglx', spikeglx_folder)
        RAW_RECORDING = si.read_spikeglx(spikeglx_folder, stream_name=f'imec{IMEC}.ap', load_sync_channel=False)
    
        ######################################### PROCESS RAW RECORDING ##########################################
        print("Step 2: Preprocessing raw recording...")
        if plot_figs:
            print(os.path.join(figs_folder, 'noise_dists.png'))
            plot_noise_hists(RAW_RECORDING, save_path=os.path.join(figs_folder, 'noise_dists.png'))
            RECORDING = preprocess_recording(RAW_RECORDING, save_path=figs_folder)
            plot_peaks_from_recording(RECORDING, save_path=os.path.join(figs_folder, 'peak_times_depths1.png'))
        else:
            RECORDING = preprocess_recording(RAW_RECORDING)
    
        ############################################# ESTIMATE DRIFT #############################################
        if not Path(motion_folder).exists():
            print("Step 3: Estimating and applying motion correction...")
    
            rec = RECORDING.astype(float)
            rec_corrected, motion_info = si.correct_motion(rec, preset=drift_preset, interpolate_motion_kwargs={'border_mode':'force_extrapolate'},folder=motion_folder, output_motion_info=True)
            
            rec_corrected
            REC_CORRECTED = rec_corrected.astype(int)
            
            if plot_figs:
                plot_motion_correction(RECORDING, motion_info, save_path=os.path.join(figs_folder, 'motion_info.png'))
                
        else:
            print("Step 3: Motion detection already complete...")
            motion_info = si.load_motion_info(motion_folder)
            
        ######################################## SAVE CORRECTED RECORDING ########################################
        print("Step 4: Saving drift-corrected recording to disk...")

        REC_CORRECTED = REC_CORRECTED.save(folder=preprocess_folder, format='binary', dtype='int16')

        if plot_figs:
            plot_peaks_from_recording(RECORDING, save_path=os.path.join(figs_folder, 'peak_times_depths2.png'))

        write_recording_details_txt(RAW_RECORDING, preprocess_folder / 'raw_rec_output.txt')
        write_recording_details_txt(RECORDING, preprocess_folder / 'rec_output.txt')

    ############################################# RUN KILOSORT ##############################################
    params = si.get_default_sorter_params(sorter_name_or_class='kilosort4')
    params_kilosort4 = {
        'do_correction': False,
        'bad_channels': None #would need to change if we choose not to delete bad channels
    }
    
    sorting = si.run_sorter('kilosort4', REC_CORRECTED, remove_existing_folder=True, folder=preprocess_folder.parent / 'kilosort4_preprocess',
                            docker_image=False, verbose=True, **params_kilosort4)
    
    sorting
    # sorting = si.read_sorter_folder(folder+'kilosort4_output')
    
    # count elapsed time
    elapsed = time.time() - t
    elapsed
    
    print("Step 5: Done! Drift-corrected recording saved successfully.")

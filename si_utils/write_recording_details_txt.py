import spikeinterface.full as si
import os

def write_recording_details_txt(rec,save_path):
    num_channels = rec.get_num_channels()
    sampling_frequency = rec.get_sampling_frequency()
    num_segments = rec.get_num_segments()
    num_samples = rec.get_num_samples(segment_index=0)
    total_time = num_samples / sampling_frequency
    dtype = rec.get_dtype()
    
    # opening a .txt file to output the values of raw_rec
    with open(save_path, 'w') as file:
        # Step 4: Write the metadata to the file
        file.write(f'Number of channels: {num_channels}\n')
        file.write(f'Sampling frequency: {sampling_frequency} Hz\n')
        file.write(f'Number of segments: {num_segments}\n')
        file.write(f'Number of samples: {num_samples}\n')
        file.write(f'Total time: {total_time} seconds\n')
        file.write(f'Data type: {dtype}\n')

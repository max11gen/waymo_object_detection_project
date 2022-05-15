import argparse
import glob
import os
import random

import numpy as np

from utils import get_module_logger


def split(data_dir):
    """
    Create three splits from the processed records. The files should be moved to new folders in the 
    same directory. This folder should be named train, val and test.

    args:
        - data_dir [str]: data directory, /home/workspace/data/waymo
    """
    source_path = data_dir + '/training_and_validation'
    destination_paths = ['/train', '/val', '/test']
    destination_paths = [data_dir + s for s in destination_paths]
    total_folder_size = get_folder_size(source_path)
    set_sizes = [0.8, 0.1, 0.1]
    set_sizes = np.cumsum(set_sizes).tolist()
    size_of_processed_files = 0
    current_path_ind=0
    for path, dirs, files in os.walk(source_path):
        for f in files:
            file_size = os.path.getsize(os.path.join(path, f))
            size_of_processed_files += file_size
            os.rename(os.path.join(path, f),os.path.join(destination_paths[current_path_ind],f))
            if(size_of_processed_files > set_sizes[current_path_ind]*total_folder_size):
                current_path_ind += 1
            


def get_folder_size(folder):
    size = 0
 
    # get size
    for path, dirs, files in os.walk(folder):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)

    return size        
 

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Split data into training / validation / testing')
    parser.add_argument('--data_dir', required=True,
                        help='data directory')
    args = parser.parse_args()

    logger = get_module_logger(__name__)
    logger.info('Creating splits...')
    split(args.data_dir)
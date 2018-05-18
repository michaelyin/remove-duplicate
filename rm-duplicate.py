# checkDuplicates.py
# Python 2.7.6

"""
Given a folder, walk through all files within the folder and subfolders
and get list of all files that are duplicates
The md5 checcksum for each file will determine the duplicates
"""

import os
import hashlib
from collections import defaultdict
import csv

src_folder = "/home/michael/PycharmProjects/im2markup-prep/data/batch/formula_images"


def generate_md5(fname, chunk_size=1024):
    """
    Function which takes a file name and returns md5 checksum of the file
    """
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        # Read the 1st block of the file
        chunk = f.read(chunk_size)
        # Keep reading the file until the end and update hash
        while chunk:
            hash.update(chunk)
            chunk = f.read(chunk_size)

    # Return the hex checksum
    return hash.hexdigest()


if __name__ == "__main__":
    """
    Starting block of script
    """

    # The dict will have a list as values
    md5_dict = defaultdict(list)

    file_types_inscope = ["png"]

    cnt = 0
    # Walk through all files and folders within directory
    for path, dirs, files in os.walk(src_folder):
        cnt = cnt + 1
        print("Analyzing {}".format(path))
        for each_file in files:
            print 'handle number', cnt, each_file
            if each_file.split(".")[-1].lower() in file_types_inscope:
                # The path variable gets updated for each subfolder
                file_path = os.path.join(os.path.abspath(path), each_file)
                # If there are more files with same checksum append to list
                md5 = generate_md5(file_path)
                if md5 in md5_dict:
                    #remove file
                    os.remove(file_path)
                else:
                    md5_dict[generate_md5(file_path)].append(file_path)



    print("Done")
    print 'total images: ', len(md5_dict)
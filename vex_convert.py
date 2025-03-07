# coding=utf-8
"""
I have nothing to say, it is a very simple program works
"""
import json
import tarfile
import base64
import os


def extract_vex(vex_file_location: str, temp_location: str, progress):
    """

    :param vex_file_location: the .vex file location, should include the .vex file
    :param temp_location:  the temp folder location
    :param progress:  optional way to output the progress
    """

    if not os.path.isdir(temp_location):
        os.mkdir(temp_location)
    progress("extracting json from .vex tar file")
    with tarfile.open(vex_file_location) as vex_file:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(vex_file, temp_location)
    progress("json extracted")


def pack_vex(save_folder_location: str, save_file_name: str, temp_location: str, progress):
    """

    :param save_folder_location: the .vex file location, should include the .vex file
    :param save_file_name: the .vex file name
    :param temp_location:  the temp folder location
    :param progress:  optional way to output the progress
    """
    try:
        os.remove(save_folder_location + "/" + save_file_name)
    except:
        progress("Not a replace or it is a error")

    progress("pack json into .vex")
    with tarfile.open(save_folder_location + "/" + save_file_name, "w") as vex_file:
        vex_file.add(
            temp_location +
            "/___ThIsisATemPoRaRyFiLE___.json",
            "/___ThIsisATemPoRaRyFiLE___.json")
    progress("packing done!")


def decode_json(code_folder_location: str, temp_location: str, progress):
    """

    :param code_folder_location: should be a folder dedicated for code files
    :param temp_location: the temp folder for .json
    :param progress: the output for progress, on console it should be "print"
    """
    progress("loading json")
    with open(temp_location + "/___ThIsisATemPoRaRyFiLE___.json") as content:
        dot_vex_json: dict = json.load(content)
        progress("extracting and decode files from json")
        for x in dot_vex_json["files"]:
            with open(code_folder_location + "/" + x, "wb") as file:
                file.write(base64.b64decode(dot_vex_json["files"][x]))
    progress(str(len(dot_vex_json["files"])) + "Files extracted")


def update_json(code_folder: str, temp_location: str, progress):
    """

    :param code_folder: the files you want to put into the .vex
    :param temp_location: the folder containing ___ThIsisATemPoRaRyFiLE___.json
    :param progress: optional way to output the progress
    """
    progress("loading json")
    with open(temp_location + "/___ThIsisATemPoRaRyFiLE___.json") as content:
        dot_vex_json: dict = json.load(content)
        encode_files: list = os.listdir(code_folder)
        progress("replacing file inside json")
        for x in encode_files:
            with open(code_folder + "/" + x, "rb") as file:
                dot_vex_json["files"][x] = base64.b64encode(file.read()).decode("utf-8")
    progress("replace the json file")
    try:
        os.remove(temp_location + "/___ThIsisATemPoRaRyFiLE___.json")
    except:
        progress("failed to remove old json file")
    with open(temp_location + "/___ThIsisATemPoRaRyFiLE___.json", "w") as content:
        json.dump(dot_vex_json, content)
    progress("replace/update json complete")


def main():
    """
    I have no idea why someone try to run this and say it is not working....
    """
    print("IT IS NOT WORKING")

if __name__ == '__main__':
    main()

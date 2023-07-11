import os
from box.exceptions import BoxValueError
import yaml
from src.cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Read a yaml file and return a ConfigBox object.

    Args:
        path_to_yaml (str): Path to the yaml file.

    Raises:
        ValueError: If the yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError(f"yaml file is empty")
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories: list, verbos=True):
    """Create a list of directories

    Args:
        path_to_directories (list): list of directories
        ignore_logs (bool, optional): ignore if multiple directories is to be created. Default is False
    """

    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbos:
            logger.info(f"Created directory as {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """Save a json data

    Args:  
        path (str): path to save the json
        data (dict): data to be saved in json file

    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    
    logger.info(f"json file saved at: {path}")

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Load a json file

    Args:
        path (Path): path to the json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path, "r") as f:
        content = json.load(f)
    return ConfigBox(content)

@ensure_annotations
def save_bin(path: Path, data: Any):
    """Save a binary file  

    Args:
        path (str): path to save the binary file
        data (Any): data to be saved in binary file
    
    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")

@ensure_annotations
def load_bin(path: Path) -> Any:
    """Load a binary file

    Args:
        path (Path): path to the binary file

    Returns:
        Any: object stored in the binary file
    """
    data = joblib.load(value=path)
    logger.info(f"binary file loaded at: {path}")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"


def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())

    
    
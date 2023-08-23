"""Utils for file I/O.
"""

import json
import pickle
import logging
from pathlib import Path

import cloudpickle


def save_pickle(obj: object, path: str | Path, overwrite: bool = True) -> bool:
    """Saves the given object as a pickle with the given file path.

    Uses `cloudpickle` to be able to save objects that standard `pickle` would
    find unpicklable.

    Parameters
    ----------
    obj : object
        The object to pickle
    path : str or Path
        The file path to save the pickle to.

    Returns
    -------
    success : bool
        Whether pickling was successful.
    """
    try:
        with open(path, "wb" if overwrite else "xb") as f_out:
            cloudpickle.dump(obj, f_out)
            return True

    except Exception as e:
        logging.error(f"Pickling failed with exception '{e}'")
        return False


def load_pickle(path: str | Path) -> object:
    with open(path, "rb") as f_in:
        return pickle.load(f_in)


def load_json(path: str | Path) -> object:
    with open(path, "r") as f_in:
        return json.load(f_in)


def save_json(obj: object, path: str | Path, overwrite: bool = True):
    logging.info(f"Saving JSON file to '{str(path)}'")
    with open(path, "w" if overwrite else "x") as f_out:
        json.dump(obj, f_out, indent=4, sort_keys=True)

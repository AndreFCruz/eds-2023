import logging
from pathlib import Path

import cloudpickle


def save_pickle(obj: object, path: str | Path, overwrite: bool = True) -> bool:
    """Saves the given object as a pickle with the given file path.

    Parameters
    ----------
    obj : object
        The object to pickle
    path : str or Path
        The file path to save the pickle with.

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

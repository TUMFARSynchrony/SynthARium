"""Provide utility functions used by different parts of the software."""

import csv
import os
import uuid
import time
import platform


def generate_unique_id(existing_ids: list[str]):
    """Generate an unique id without collision with `existing_ids`.

    Parameters
    ----------
    existing_ids : list of str
        Existing ids which may not include the new, generated id.

    Returns
    -------
    str
        Unique id generated.

    See Also
    --------
    SessionManager._generate_unique_session_id : Generate an unique session
        id.
    """
    id = uuid.uuid4().hex[:10]
    while id in existing_ids:
        id = uuid.uuid4().hex[:10]
    return id


def get_system_specs() -> dict:
    """Get general system specs / info."""
    return {
        "python_version": platform.python_version(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "platform": platform.platform(),
        "processor": platform.processor(),
        "cpu_count": os.cpu_count(),
    }


def timestamp() -> int:
    """Get the current time in milliseconds since January 1, 1970, 00:00:00 (UTC)."""
    return round(time.time() * 1000)

def write_csv_file(output_filename: str, data: list, headers: list):
    """Write data into csv file."""
    try:
        with open(output_filename, "w+") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
    except FileNotFoundError:
        print("Output file not present", output_filename)
        print("Current dir: ", os.getcwd())
        raise FileNotFoundError
    
def get_sessions_path():
    """Get sessions folder path."""
    return os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "sessions"
        )
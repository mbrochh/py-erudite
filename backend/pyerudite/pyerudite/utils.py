"""Project wide utility functions."""

import datetime
import os
import re


def clean_title(value):
    """
    Removes `:/\`, which are characters that Obisidon (and operating systems)
    do not like for filenames.

    """
    value = re.sub(r" ?[:/\\] ?", " - ", value)
    return value


def slugify(value):
    """
    Normalizes a string: converts to lowercase, removes non-alpha characters,
    and converts dashes and spaces to underscores.

    """
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    value = re.sub(r"[-\s]+", "_", value)
    return re.sub(r"[^\x00-\x7f]", "", value)


def get_slugified_filename(file_path):
    """
    Separates file path from filename and returns slugified filename.

    :file_path: Full file path.

    :returns: Tuple of `(slugified filename, lowercase file extension)`.

    """
    original_path, original_filename = os.path.split(file_path)
    original_file_base, file_ext = os.path.splitext(original_filename)
    slugified_base = slugify(original_file_base)
    file_ext = file_ext.lower()
    return slugified_base, file_ext


def timestamp():
    return str(datetime.datetime.now())[:19]

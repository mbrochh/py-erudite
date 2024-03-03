"""Tests for the utils module."""

import pytest

from .. import utils


@pytest.mark.parametrize(
    "title,expected",
    [
        ("Title 1", "Title 1"),
        ("Title:1", "Title - 1"),
        ("Title: 1", "Title - 1"),
        ("Title / 1", "Title - 1"),
        ("Title \ 1", "Title - 1"),
    ],
)
def test_clean_title(title, expected):
    """Tests for the clean_title() function."""
    res = utils.clean_title(title)
    assert res == expected

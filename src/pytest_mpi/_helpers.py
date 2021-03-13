"""
Internal helpers for testing only, do not use in main code
"""
import pytest


def _fix_plural(**kwargs):
    """
    Work around error -> errors change in pytest 6
    """
    if int(pytest.__version__[0]) >= 6:
        return kwargs
    if "errors" in kwargs:
        errors = kwargs.pop("errors")
        kwargs["error"] = errors
    return kwargs

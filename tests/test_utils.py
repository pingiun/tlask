import pytest

import os

from tlask.utils import _endpoint_from_view_func, import_string, get_root_path

def test__endpoint_from_view_func():
    def test_func():
        pass
    assert _endpoint_from_view_func(test_func) == 'test_func'

def test__endpoint_from_view_func_none():
    with pytest.raises(AssertionError):
        _endpoint_from_view_func(None)

def test_import_string():
    assert import_string('random') is not None

def test_import_string_import_error():
    with pytest.raises(ImportError):
        import_string('test.fail')

def test_import_string_import_config():
    import_string('config.testuser') == 167921906

def test_get_root_path():
    assert get_root_path('__main__')

def test_get_root_path_fail():
    assert get_root_path('') == os.getcwd()
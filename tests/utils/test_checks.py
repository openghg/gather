from gather.utils import check_date, check_nan
import numpy as np
import pytest


def test_check_date():
    date_str = "2021-01-01"

    assert check_date(date=date_str) == date_str
    assert check_date(date="this") == "NA"
    assert check_date(date="1001") == "NA"

    unix_timestamp_ms = 1636043284779

    assert check_date(unix_timestamp_ms) == unix_timestamp_ms


def test_check_nan():
    assert check_nan(data=np.nan)
    assert check_nan(data=123) == 123

    with pytest.raises(TypeError):
        check_nan(data="123") == "123"
        assert check_nan(data=None)

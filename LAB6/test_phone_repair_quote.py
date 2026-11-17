import pytest
from phone_repair_quote import repair_quote, repair_days, trade_in_value

# Example starter test cases
def test_budget_screen():
    assert repair_quote("screen", "budget", False, False) == 4600

def test_in_stock_quick():
    assert repair_days("battery", True, 2) == 1

# Additional test cases for 100% code & branch coverage
def test_quote_unknown_part():
    with pytest.raises(ValueError, match="unknown part"):
        repair_quote("display", "budget", False, False)

def test_quote_unknown_brand_tier():
    with pytest.raises(ValueError, match="unknown brand tier"):
        repair_quote("screen", "premium", False, False)

def test_quote_flagship_screen_express():
    assert repair_quote("screen", "flagship", True, True) == 9100

def test_quote_battery_under_warranty():
    assert repair_quote("battery", "budget", True, False) == 300

def test_quote_camera_not_under_warranty_express():
    assert repair_quote("camera", "budget", False, True) == 3300

def test_repair_days_zero_technicians_screen():
    assert repair_days("screen", False, 0) == 8

def test_repair_days_technicians_free_camera():
    assert repair_days("camera", False, 2) == 6

def test_repair_days_battery_out_of_stock():
    assert repair_days("battery", False, 1) == 3

def test_trade_in_invalid_price():
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(0, 10, False)

def test_trade_in_invalid_age():
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(10000, -1, False)

def test_trade_in_expired():
    assert trade_in_value(50000, 50, False) == 0

def test_trade_in_under_12_months_cracked():
    assert trade_in_value(10000, 6, True) == 3000

def test_trade_in_under_12_months_uncracked():
    assert trade_in_value(10000, 12, False) == 6000

def test_trade_in_between_12_and_24_months():
    assert trade_in_value(10000, 18, False) == 4000

def test_trade_in_over_24_months():
    assert trade_in_value(10000, 36, False) == 2000

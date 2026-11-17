import pytest
from phone_repair_quote import repair_quote, repair_days, trade_in_value

# Tests for repair_quote (Line Coverage)
def test_quote_unknown_part():
    with pytest.raises(ValueError, match="unknown part"):
        repair_quote("speaker", "budget", False, False)

def test_quote_unknown_brand_tier():
    with pytest.raises(ValueError, match="unknown brand tier"):
        repair_quote("screen", "premium", False, False)

def test_quote_flagship_screen_express():
    # Covers flagship tier, screen labour, and express delivery
    assert repair_quote("screen", "flagship", False, True) == 9100

def test_quote_budget_battery_warranty():
    # Covers non-screen labour (300) and warranty cost waiver (0)
    assert repair_quote("battery", "budget", True, False) == 300

# Tests for repair_days (Line Coverage)
def test_repair_days_zero_technicians_screen_out_of_stock():
    # Covers technicians_free == 0 (3 days) and screen out of stock (+5 days)
    assert repair_days("screen", False, 0) == 8

def test_repair_days_available_technicians_battery_out_of_stock():
    # Covers technicians_free > 0 (1 day) and non-screen/non-camera out of stock (+2 days)
    assert repair_days("battery", False, 2) == 3

def test_repair_days_in_stock():
    # Covers parts in stock path (1 day)
    assert repair_days("camera", True, 1) == 1

# Tests for trade_in_value (Line Coverage)
def test_trade_in_invalid_price():
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(0, 10, False)

def test_trade_in_invalid_age():
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(10000, -1, False)

def test_trade_in_expired():
    # Age > 48 months returns 0
    assert trade_in_value(50000, 50, False) == 0

def test_trade_in_under_12_months_cracked():
    # Age <= 12 months (60%) and screen_cracked reduction (// 2)
    assert trade_in_value(10000, 6, True) == 3000

def test_trade_in_between_12_and_24_months():
    # 12 < Age <= 24 months (40%)
    assert trade_in_value(10000, 18, False) == 4000

def test_trade_in_over_24_months():
    # Age > 24 months (20%)
    assert trade_in_value(10000, 36, False) == 2000

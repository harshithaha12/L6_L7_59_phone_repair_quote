import pytest
from phone_repair_quote import repair_quote, repair_days, trade_in_value

# ==========================================
# Branch Coverage Tests for repair_quote
# ==========================================

def test_branch_quote_unknown_part():
    # Branch: part not in PART_COST (True)
    with pytest.raises(ValueError, match="unknown part"):
        repair_quote("display", "budget", False, False)

def test_branch_quote_unknown_brand_tier():
    # Branch: part in PART_COST (False), brand_tier not in ("budget", "flagship") (True)
    with pytest.raises(ValueError, match="unknown brand tier"):
        repair_quote("screen", "midrange", False, False)

def test_branch_quote_flagship_screen_express():
    # Branches:
    # - brand_tier == "flagship" (True: cost doubled)
    # - part == "screen" (True: labour = 600)
    # - under_warranty and part != "screen" (False: part == "screen")
    # - express (True: +500)
    # 4000*2 + 600 + 500 = 9100
    assert repair_quote("screen", "flagship", True, True) == 9100

def test_branch_quote_budget_screen_no_express():
    # Branches:
    # - brand_tier == "flagship" (False: budget)
    # - part == "screen" (True: labour = 600)
    # - under_warranty and part != "screen" (False: not under warranty)
    # - express (False)
    # 4000 + 600 = 4600
    assert repair_quote("screen", "budget", False, False) == 4600

def test_branch_quote_battery_under_warranty():
    # Branches:
    # - brand_tier == "flagship" (False)
    # - part == "screen" (False: labour = 300)
    # - under_warranty and part != "screen" (True: cost = 0)
    # - express (False)
    # 0 + 300 = 300
    assert repair_quote("battery", "budget", True, False) == 300

def test_branch_quote_camera_not_under_warranty_express():
    # Branches:
    # - brand_tier == "flagship" (False)
    # - part == "screen" (False: labour = 300)
    # - under_warranty and part != "screen" (False: under_warranty is False)
    # - express (True: +500)
    # 2500 + 300 + 500 = 3300
    assert repair_quote("camera", "budget", False, True) == 3300


# ==========================================
# Branch Coverage Tests for repair_days
# ==========================================

def test_branch_repair_days_zero_technicians_screen_out_of_stock():
    # Branches:
    # - technicians_free == 0 (True: days = 3)
    # - not parts_in_stock (True)
    # - part == "screen" (True: +5 days) -> 8
    assert repair_days("screen", False, 0) == 8

def test_branch_repair_days_technicians_free_camera_out_of_stock():
    # Branches:
    # - technicians_free == 0 (False: days = 1)
    # - not parts_in_stock (True)
    # - part == "screen" (False), part == "camera" (True: +5 days) -> 6
    assert repair_days("camera", False, 2) == 6

def test_branch_repair_days_battery_out_of_stock():
    # Branches:
    # - technicians_free == 0 (False: days = 1)
    # - not parts_in_stock (True)
    # - part == "screen" or part == "camera" (False: other part: +2 days) -> 3
    assert repair_days("battery", False, 1) == 3

def test_branch_repair_days_parts_in_stock():
    # Branches:
    # - technicians_free == 0 (False: days = 1)
    # - not parts_in_stock (False: in stock) -> 1
    assert repair_days("charging_port", True, 3) == 1


# ==========================================
# Branch Coverage Tests for trade_in_value
# ==========================================

def test_branch_trade_in_invalid_price_zero():
    # Branch: original_price <= 0 (True)
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(0, 12, False)

def test_branch_trade_in_invalid_price_negative():
    # Branch: original_price <= 0 (True)
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(-5000, 12, False)

def test_branch_trade_in_invalid_age_negative():
    # Branch: original_price <= 0 (False), age_months < 0 (True)
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(20000, -1, False)

def test_branch_trade_in_age_exceeds_48():
    # Branch: age_months > 48 (True) -> 0
    assert trade_in_value(50000, 49, False) == 0

def test_branch_trade_in_under_12_months_uncracked():
    # Branches:
    # - age_months > 48 (False)
    # - age_months <= 12 (True: 60%)
    # - screen_cracked (False)
    # 10000 * 60 // 100 = 6000
    assert trade_in_value(10000, 12, False) == 6000

def test_branch_trade_in_under_12_months_cracked():
    # Branches:
    # - age_months <= 12 (True: 60%)
    # - screen_cracked (True: // 2)
    # 10000 * 60 // 100 // 2 = 3000
    assert trade_in_value(10000, 6, True) == 3000

def test_branch_trade_in_between_12_and_24_months():
    # Branches:
    # - age_months <= 12 (False)
    # - age_months <= 24 (True: 40%)
    # - screen_cracked (False)
    # 10000 * 40 // 100 = 4000
    assert trade_in_value(10000, 24, False) == 4000

def test_branch_trade_in_over_24_months():
    # Branches:
    # - age_months <= 12 (False)
    # - age_months <= 24 (False: else: 20%)
    # - screen_cracked (False)
    # 10000 * 20 // 100 = 2000
    assert trade_in_value(10000, 36, False) == 2000

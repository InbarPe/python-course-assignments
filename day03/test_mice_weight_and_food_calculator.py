import pytest
from mice_weight_and_food_calculator_core import percent_and_food_weight


def test_percent_weight_calculation():
    """Test that percent weight is calculated correctly."""
    current = 20.0
    initial = 25.0
    percent, food = percent_and_food_weight(current, initial)
    assert percent == 80.0, f"Expected 80.0%, got {percent}%"


def test_food_weight_calculation_above_25g():
    """Test food weight for mouse above 25g."""
    current = 30.0
    initial = 30.0
    percent, food = percent_and_food_weight(current, initial)
    # 2.5g per 25g → 30g should get 3.0g
    assert food == 3.0, f"Expected 3.0g, got {food}g"


def test_food_weight_calculation_below_25g():
    """Test food weight for mouse below 25g (should be minimum 2.5g)."""
    current = 20.0
    initial = 25.0
    percent, food = percent_and_food_weight(current, initial)
    # Below 25g gets minimum 2.5g
    assert food == 2.5, f"Expected 2.5g, got {food}g"


def test_food_weight_at_25g():
    """Test food weight exactly at 25g."""
    current = 25.0
    initial = 25.0
    percent, food = percent_and_food_weight(current, initial)
    assert food == 2.5, f"Expected 2.5g, got {food}g"


def test_percent_weight_low_warning():
    """Test that percent weight below 80% is identified."""
    current = 19.0
    initial = 25.0
    percent, food = percent_and_food_weight(current, initial)
    assert percent < 80, f"Expected percent < 80%, got {percent}%"


def test_percent_weight_good():
    """Test that percent weight at 80% or above is good."""
    current = 20.0
    initial = 25.0
    percent, food = percent_and_food_weight(current, initial)
    assert percent >= 80, f"Expected percent >= 80%, got {percent}%"


def test_equal_weights():
    """Test when current weight equals initial weight (100%)."""
    current = 25.0
    initial = 25.0
    percent, food = percent_and_food_weight(current, initial)
    assert percent == 100.0, f"Expected 100%, got {percent}%"


def test_percent_weight_above_100():
    """Test when current weight is above initial weight (>100%)."""
    current = 26.0
    initial = 25.0
    percent, food = percent_and_food_weight(current, initial)
    assert percent > 100.0, f"Expected > 100%, got {percent}%"
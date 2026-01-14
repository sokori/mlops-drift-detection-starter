import pytest
import pandas as pd
import numpy as np

# tests/test_drift.py
from src.compare_data import calculate_drift_logic

def test_drift_detection_math():
    # Test Case 1: Drift should be detected (10 -> 20 is 100% change)
    score, is_drifted = calculate_drift_logic(10, 20, 0.2)
    assert is_drifted is True
    assert score == 1.0

    # Test Case 2: Healthy (10 -> 11 is 10% change, below 20% threshold)
    score, is_drifted = calculate_drift_logic(10, 11, 0.2)
    assert is_drifted is False
    assert score == 0.1

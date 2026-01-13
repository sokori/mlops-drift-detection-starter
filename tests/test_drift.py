# tests/test_drift.py
import pytest
import pandas as pd
import numpy as np
from src.compare_data import calculate_drift_logic # Adjust this import based on your actual function name

def test_drift_detection_math():
    # Test Case 1: Drift should be detected (10 -> 20 is 100% change)
    score, is_drifted = calculate_drift_logic(10, 20, 0.2)
    assert is_drifted == True
    assert score == 1.0
    
    # Assuming your function returns (score, is_drifted)
   score, is_drifted = calculate_drift_logic(10, 11, 0.2)
    assert is_drifted == False
    assert score == 0.1

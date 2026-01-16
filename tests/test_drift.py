from src.compare_data import calculate_drift_logic

def test_drift_detection_math():
    # Case 1: Drift
    score1, drift1 = calculate_drift_logic(10.0, 20.0, 0.2)
    assert drift1 == True
    
    # Case 2: Healthy
    score2, drift2 = calculate_drift_logic(10.0, 11.0, 0.2)
    assert drift2 == False

# day1_historian_hysteria/tests/test_hysteria.py

import pytest
from day1_historian_hysteria.hysteria import (
    parse_input,
    compute_total_distance,
    compute_similarity_score
)

def test_parse_input():
    input_data = """
    1 2
    3 4
    5 6
    """
    expected_left = [1, 3, 5]
    expected_right = [2, 4, 6]
    left, right = parse_input(input_data)
    assert left == expected_left, "Left list does not match expected output."
    assert right == expected_right, "Right list does not match expected output."

def test_parse_input_invalid_line():
    input_data = """
    1 2
    3
    4 5
    """
    with pytest.raises(ValueError) as exc_info:
        parse_input(input_data)
    assert "Invalid line format" in str(exc_info.value), "Did not raise ValueError for invalid line."

def test_compute_total_distance_basic():
    left = [1, 2, 3]
    right = [4, 5, 6]
    # Sorted left: [1,2,3]
    # Sorted right: [4,5,6]
    # Differences: |1-4| + |2-5| + |3-6| = 3 + 3 + 3 = 9
    expected_distance = 9
    distance = compute_total_distance(left, right)
    assert distance == expected_distance, "Total distance calculation is incorrect."

def test_compute_total_distance_unsorted_input():
    left = [3, 1, 2]
    right = [6, 4, 5]
    # Sorted left: [1,2,3]
    # Sorted right: [4,5,6]
    # Differences: |1-4| + |2-5| + |3-6| = 3 + 3 + 3 = 9
    expected_distance = 9
    distance = compute_total_distance(left, right)
    assert distance == expected_distance, "Total distance with unsorted input is incorrect."

def test_compute_total_distance_empty_lists():
    left = []
    right = []
    # According to the implementation, this should return 0, not raise an error
    expected_distance = 0
    distance = compute_total_distance(left, right)
    assert distance == expected_distance, "Total distance with empty lists should be 0."

def test_compute_similarity_score_basic():
    left = [1, 2, 3]
    right = [2, 3, 2, 4]
    # Counter for right: {2:2, 3:1, 4:1}
    # Similarity score: 1*0 + 2*2 + 3*1 = 0 + 4 + 3 = 7
    expected_score = 7
    score = compute_similarity_score(left, right)
    assert score == expected_score, f"Similarity score calculation is incorrect. Expected {expected_score}, got {score}."

def test_compute_similarity_score_no_overlap():
    left = [1, 2]
    right = [3, 4]
    # No overlapping numbers
    expected_score = 0
    score = compute_similarity_score(left, right)
    assert score == expected_score, "Similarity score with no overlapping numbers is incorrect."

def test_compute_similarity_score_multiple_frequencies():
    left = [2, 3, 2]
    right = [2, 2, 3]
    # Counter for right: {2:2, 3:1}
    # Similarity score: 2*2 + 3*1 + 2*2 = 4 + 3 + 4 = 11
    expected_score = 11
    score = compute_similarity_score(left, right)
    assert score == expected_score, "Similarity score with multiple frequencies is incorrect."

def test_compute_similarity_score_empty_lists():
    left = []
    right = []
    expected_score = 0
    score = compute_similarity_score(left, right)
    assert score == expected_score, "Similarity score with empty lists should be 0."

def test_compute_similarity_score_left_empty():
    left = []
    right = [1, 2, 3]
    expected_score = 0
    score = compute_similarity_score(left, right)
    assert score == expected_score, "Similarity score should be 0 when left list is empty."

def test_compute_similarity_score_right_empty():
    left = [1, 2, 3]
    right = []
    expected_score = 0
    score = compute_similarity_score(left, right)
    assert score == expected_score, "Similarity score should be 0 when right list is empty."
# tests/test_scanner.py
import pytest
from bias_radar.scanner import BiasScanner

def test_calculate_bias_score():
    scanner = BiasScanner()
    score = scanner.calculate_bias_score(0.8, 0.2)
    assert score == 0.8

def test_calculate_bias_score_equal():
    scanner = BiasScanner()
    score = scanner.calculate_bias_score(0.5, 0.5)
    assert score == 0.5

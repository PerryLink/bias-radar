import pytest
from bias_radar.visualizer import BiasVisualizer
import os


def test_visualizer_init():
    data = {"doctor": 0.85, "nurse": 0.10}
    viz = BiasVisualizer(data)
    assert viz.professions == ["doctor", "nurse"]
    assert viz.scores == [0.85, 0.10]


def test_create_radar_chart(tmp_path):
    data = {
        "doctor": 0.85,
        "nurse": 0.10,
        "engineer": 0.92,
        "teacher": 0.35,
        "receptionist": 0.15,
        "programmer": 0.88
    }

    output_path = tmp_path / "test_chart.png"
    viz = BiasVisualizer(data)
    viz.create_radar_chart(str(output_path))

    assert output_path.exists()
    assert output_path.stat().st_size > 0

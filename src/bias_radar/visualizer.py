import matplotlib.pyplot as plt
import numpy as np
from typing import Dict


class BiasVisualizer:
    def __init__(self, data: Dict[str, float]):
        self.data = data
        self.professions = list(data.keys())
        self.scores = list(data.values())

    def create_radar_chart(self, output_path: str = "bias_report.png"):
        """Generate radar chart and save to file"""
        fig, ax = self._setup_radar_axes()
        self._plot_data(ax)
        self._add_styling(ax)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

    def _setup_radar_axes(self):
        """Setup polar axes for radar chart"""
        num_vars = len(self.professions)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles)
        ax.set_xticklabels(self.professions, size=12)

        return fig, ax

    def _plot_data(self, ax):
        """Plot bias scores on radar chart"""
        num_vars = len(self.professions)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        scores = self.scores + [self.scores[0]]
        angles += angles[:1]

        ax.plot(angles, scores, 'o-', linewidth=2, color='#2E86AB', label='Bias Score')
        ax.fill(angles, scores, alpha=0.25, color='#2E86AB')

        # Add neutral baseline (0.5)
        neutral = [0.5] * (num_vars + 1)
        ax.plot(angles, neutral, '--', linewidth=1.5, color='#06A77D', label='Neutral (0.5)', alpha=0.7)

    def _add_styling(self, ax):
        """Add styling and labels to chart"""
        ax.set_ylim(0, 1)
        ax.set_yticks([0.25, 0.5, 0.75, 1.0])
        ax.set_yticklabels(['0.25', '0.5', '0.75', '1.0'], size=10)
        ax.grid(True, linestyle='--', alpha=0.7)

        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)
        ax.set_title('Gender Bias Radar Chart\n(1.0 = Male bias, 0.0 = Female bias)',
                     size=14, weight='bold', pad=20)

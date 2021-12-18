import matplotlib.pyplot as plt
from Parametrs import *


class DrawForecast:
    def __init__(self):
        pass

    def draw(self, forecast):
        min_temp, max_temp, date_str = self.parse_forecast(forecast)
        fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
        ax.plot(date_str, min_temp, color=MIN_COLOR, marker=MARKER, label='Мин. темп.', linewidth=LINEWIDTH)
        ax.plot(date_str, max_temp, color=MAX_COLOR, marker=MARKER, label='Мин. темп.', linewidth=LINEWIDTH)
        ax.set_ylabel(YLABEL)
        ax.grid(color=GRID_COLOR, linestyle=GRID_LINESTYLE, linewidth=GRID_LINEWIDTH)
        plt.legend(shadow=True, fontsize=LEGEND_FONT_SIZE)
        plt.savefig(GRAPH_NAME)

    def parse_forecast(self, forecast):
        min_temp = [int(i[1].split()[1][:-1]) for i in forecast]
        max_temp = [int(i[1].split()[3][:-1]) for i in forecast]
        date_str = [i[0] for i in forecast]
        return min_temp, max_temp, date_str

# fire_visualization.py
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

class ForestFireVisualization:
    def __init__(self, model, frames):
        self.model = model
        self.frames = frames

    def animate(self):
        fig, ax = plt.subplots(figsize=(30, 30))
        plt.subplots_adjust(left=0.1, right=0.9, bottom=0.3, top=0.9)

        cmap = mcolors.ListedColormap(['green', 'orange', 'black'])
        img = ax.imshow(self.model.grid, cmap=cmap, vmin=0, vmax=2)

        ax_p_tree = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        ax_p_burn = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        ax_t_burn = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')

        s_p_tree = Slider(ax_p_tree, 'P Tree', 0.0, 1.0, valinit=0.7)
        s_p_burn = Slider(ax_p_burn, 'P Burn', 0.0, 1.0, valinit=0.1)
        s_t_burn = Slider(ax_t_burn, 'T Burn', 1, 30, valinit=15, valstep=1)

        ax_pause = plt.axes([0.1, 0.4, 0.1, 0.05])
        ax_restart = plt.axes([0.25, 0.4, 0.1, 0.05])

        pause_button = Button(ax_pause, 'Pause', hovercolor='0.975')
        restart_button = Button(ax_restart, 'Restart', hovercolor='0.975')

        def update_params(val):
            self.model.p_tree = s_p_tree.val
            self.model.p_burn = s_p_burn.val
            self.model.t_burn = s_t_burn.val
            self.model.running = False

        s_p_tree.on_changed(update_params)
        s_p_burn.on_changed(update_params)
        s_t_burn.on_changed(update_params)

        def pause(event):
            self.model.running = False

        def restart(event):
            self.model.initialize(s_p_tree.val)
            self.model.running = True

        pause_button.on_clicked(pause)
        restart_button.on_clicked(restart)

        def update(frame):
            if self.model.running:
                self.model.step()
                img.set_array(self.model.grid)
            return [img]

        animation = FuncAnimation(fig, update, frames=self.frames, blit=True)

        plt.colorbar(img, ax=ax, ticks=[0, 1, 2])

        plt.show()



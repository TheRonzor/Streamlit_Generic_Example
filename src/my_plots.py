import matplotlib.pyplot as plt


class SimpleLinePlot:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(8,4))
        #self.line_data, = self.ax.plot([],[], '-kx')
        return
    
    def update_plot(self, 
                    x_data: list, 
                    y_data: list,
                    x_label: str,
                    y_label: str,
                    x_lim: tuple = None,
                    y_lim: tuple = None,
                    x_ticks: list = None,
                    x_ticklabels: list = None,
                    y_ticks: list = None,
                    y_ticklabels: list = None,
                    style = '-kx'
                    ) -> None:
        
        self.ax.plot(x_data, y_data, style)
        
        #self.line_data.set_xdata(x_data)
        #self.line_data.set_ydata(y_data)

        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)

        if x_ticks is not None:
            self.ax.set_xticks(x_ticks)
        if y_ticks is not None:
            self.ax.set_yticks(y_ticks)
        
        if x_ticklabels is not None:
            if x_ticks is None:
                self.ax.set_xticks(range(len(x_ticklabels)))
            self.ax.set_xticklabels(x_ticklabels)
        if y_ticklabels is not None:
            if y_ticks is None:
                self.ax.set_yticks(range(len(y_ticklabels)))
            self.ax.set_yticklabels(y_ticklabels)
        
        if x_lim is not None:
            self.ax.set_xlim(x_lim)
        if y_lim is not None:
            self.ax.set_ylim(y_lim)

        #self.fig.canvas.draw()
        #self.fig.canvas.flush_events()
        return

class SimpleBarChart:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(8,4))
        return
    
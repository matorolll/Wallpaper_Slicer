import tkinter as tk
from tkinter import Canvas

class ZoomableCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<Button-4>", self._on_mousewheel)
        self.bind("<Button-5>", self._on_mousewheel)  

        self._zoom_factor = 1.0
        self._zoom_center = (0, 0)

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta == -120:
            self._zoom_out(event)
        elif event.num == 4 or event.delta == 120:
            self._zoom_in(event)

    def _zoom_in(self, event):
        self._zoom_factor *= 1.1
        self._apply_zoom(event)

    def _zoom_out(self, event):
        self._zoom_factor /= 1.1
        self._apply_zoom(event)

    def _apply_zoom(self, event):
        self.scale("all", self._zoom_center[0], self._zoom_center[1], self._zoom_factor, self._zoom_factor)
        self._zoom_center = (event.x, event.y)
        self.configure(scrollregion=self.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Zoomable Canvas Example")
    canvas = ZoomableCanvas(root, width=800, height=600, bg="white")
    canvas.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    canvas.create_rectangle(50, 50, 200, 200, fill="red")
    canvas.create_oval(300, 100, 500, 300, fill="blue")
    canvas.create_line(600, 200, 700, 400, fill="green", width=3)
    root.mainloop()

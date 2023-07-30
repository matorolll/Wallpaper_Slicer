import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class Square:
    def __init__(self, canvas, x, y, size, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.shape = self.canvas.create_rectangle(x, y, x + size, y + size, fill=color)
        self.canvas.tag_bind(self.shape, '<B1-Motion>', self.move)

    def move(self, event):
        dx = event.x - self.x - self.size // 2
        dy = event.y - self.y - self.size // 2
        self.canvas.move(self.shape, dx, dy)
        self.x += dx
        self.y += dy

class ImageOverlapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Overlap App")

        self.canvas_width = 500
        self.canvas_height = 500

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()

        self.squares = []
        self.create_squares()

        self.canvas.bind('<ButtonRelease-1>', self.check_overlap)

        self.save_button = tk.Button(root, text="Zapisz", command=self.save_overlap)
        self.save_button.pack()

    def create_squares(self):
        colors = ['red', 'green', 'blue']
        for i, color in enumerate(colors):
            square_size = 100
            x = i * 150 + 50
            y = 200
            square = Square(self.canvas, x, y, square_size, color)
            self.squares.append(square)

    def check_overlap(self, event):
        overlap_image = Image.new("RGBA", (self.canvas_width, self.canvas_height))
        for square in self.squares:
            img = Image.new("RGBA", (square.size, square.size), square.color)
            overlap_image.paste(img, (square.x, square.y), img)

        self.overlap_image = overlap_image

    def save_overlap(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.overlap_image.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageOverlapApp(root)
    root.mainloop()

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

        self.load_image()
        self.canvas.lower(self.image_item)  # Przesuwamy obraz na spód, pod kwadraty

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

    def load_image(self):
        self.image = Image.open("obraz.png")
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_item = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

    def check_overlap(self):
        overlap_images = []
        for i, square in enumerate(self.squares):
            overlap_image = Image.new("RGBA", (self.canvas_width, self.canvas_height))
            img = Image.new("RGBA", (square.size, square.size), square.color)
            overlap_image.paste(img, (square.x, square.y), img)

            cropped_image = self.image.crop((square.x, square.y, square.x + square.size, square.y + square.size))
            alpha = overlap_image.split()[3]  # Pobieramy kanał alpha (wartość przezroczystości)
            cropped_image.paste(overlap_image, (0, 0), alpha)  # Nakładamy obraz z kanałem alpha na obraz tła

            overlap_images.append(cropped_image)

        return overlap_images

    def save_overlap(self):
        overlap_images = self.check_overlap()
        for i, cropped_image in enumerate(overlap_images):
            file_path = f"img{i+1}.png"
            cropped_image.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageOverlapApp(root)
    root.mainloop()

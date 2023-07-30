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
        self.canvas.tag_bind(self.shape, '<ButtonPress-1>', self.start_move)
        self.canvas.tag_bind(self.shape, '<B1-Motion>', self.move)
        self.canvas.tag_bind(self.shape, '<ButtonRelease-1>', self.stop_move)

        self.drag_data = {'x': 0, 'y': 0, 'item': None}

    def start_move(self, event):
        self.drag_data['item'] = self.shape
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y

    def move(self, event):
        dx = event.x - self.drag_data['x']
        dy = event.y - self.drag_data['y']
        new_x = self.x + dx
        new_y = self.y + dy

        # Sprawdzamy, czy nowe położenie nie koliduje z innymi kwadratami
        if not self.is_collision(new_x, new_y):
            self.canvas.move(self.shape, dx, dy)
            self.x = new_x
            self.y = new_y

        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y

    def stop_move(self, event):
        # Przesuwamy kwadrat do najbliższego wolnego miejsca
        new_x = (self.x + self.size // 2) // 100 * 100
        new_y = (self.y + self.size // 2) // 100 * 100

        # Sprawdzamy, czy nowe położenie nie koliduje z innymi kwadratami
        if not self.is_collision(new_x, new_y):
            dx = new_x - self.x
            dy = new_y - self.y
            self.canvas.move(self.shape, dx, dy)
            self.x = new_x
            self.y = new_y

    def is_collision(self, x, y):
        overlap = False
        for square in self.canvas.find_all():
            if square != self.shape and self.canvas.type(square) == "rectangle":
                x1, y1, x2, y2 = self.canvas.coords(square)
                if x < x2 and x + self.size > x1 and y < y2 and y + self.size > y1:
                    overlap = True
                    break
        return overlap

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
        self.image = self.image.resize((self.canvas_width, self.canvas_height), Image.ANTIALIAS)
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

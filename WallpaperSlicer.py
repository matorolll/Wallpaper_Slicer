import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
from tkinter import filedialog
import os

class Square:
    def __init__(self, canvas, x, y, width, height, color, tag, zoom_factor):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tag = tag
        self.color = color
        self.zoom_factor = zoom_factor
    
        self.x_relative_to_mouse = None
        self.y_relative_to_mouse = None


        self.shape = self.canvas.create_rectangle(x,
                                                  y,
                                                  x + (width * zoom_factor),
                                                  y + (height * zoom_factor),
                                                  stipple="gray50",
                                                  outline='red',
                                                  fill=color,
                                                  tag=[tag, 'Square'],
                                                  width=2)

        self.canvas.tag_bind(self.shape, '<B1-Motion>', self.move)
        self.canvas.tag_bind(self.shape, '<Button-1>', self.get_mouse_position)
        self.canvas.tag_bind(self.shape, '<Double-Button-1>', self.on_double_click)
        self.canvas.tag_bind(self.shape, '<ButtonRelease-1>', self.collision_handler)


    def update(self):
        self.canvas.coords( self.shape,
                            self.x,
                            self.y,
                            self.x + (self.width * self.zoom_factor),
                            self.y + (self.height * self.zoom_factor))
        
    def remove(self,tag):
        self.canvas.delete(self.canvas.find_withtag(tag))


    def get_mouse_position(self, event):
        self.x_relative_to_mouse = event.x
        self.y_relative_to_mouse = event.y


    def move(self, event):
        if self.x_relative_to_mouse is not None and self.y_relative_to_mouse is not None:
            dx = event.x - self.x_relative_to_mouse
            dy = event.y - self.y_relative_to_mouse
            self.canvas.move(self.shape, dx, dy)
            self.x_relative_to_mouse = event.x
            self.y_relative_to_mouse = event.y
            self.x += dx
            self.y += dy
            

    def change_zoom_factor(self, zoom_factor):
        self.zoom_factor = zoom_factor
        self.collision_handler()
        self.update()

    def on_double_click(self, event):
        app.on_double_click_create_app_boxes(self)


    def collision_handler(self, *args):
        anit_loop_counter = 0
        while True:
            overlapping_objects = self.canvas.find_overlapping(
                self.x,
                self.y,
                self.x + (self.width * self.zoom_factor),
                self.y + (self.height * self.zoom_factor))
            overlapping_objects = [obj for obj in overlapping_objects if obj != self.shape]
            overlapping_squares = [obj for obj in overlapping_objects if 'Square' in self.canvas.gettags(obj)]
            if not overlapping_squares: break

            obj = overlapping_squares[0]
            bbox = self.canvas.bbox(obj)
            obj_center_x = (bbox[0] + bbox[2]) / 2
            obj_center_y = (bbox[1] + bbox[3]) / 2
            square_center_x = self.x + self.width * self.zoom_factor / 2
            square_center_y = self.y + self.height * self.zoom_factor / 2
            dx = obj_center_x - square_center_x
            dy = obj_center_y - square_center_y

            if abs(dx) > abs(dy):
                if dx < 0: self.x += 1
                else: self.x -= 1
            else:
                if dy < 0:  self.y += 1
                else: self.y -= 1

            anit_loop_counter += 1
            if anit_loop_counter == 100:
                self.y -= 1
                self.x -= 1
                anit_loop_counter = 0
            self.update()
        self.update()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Wallpaper Spacer")
        self.geometry(f"{1100}x{700}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Side panel", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Load monitors info", command=self.getting_screen_data)
        self.sidebar_button_1.grid(row=1, column=0, pady=5)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Upload Image", command=self.getting_image_data)
        self.sidebar_button_2.grid(row=2, column=0, pady=5)   
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Generate", command=self.save_overlap)
        self.sidebar_button_3.grid(row=3, column=0, pady=(5,15)) 

        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Load last settings", command=self.load_square_locations_from_file)
        self.sidebar_button_4.grid(row=4, column=0, pady=5) 
        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text="Save settings", command=self.save_square_locations_to_file)
        self.sidebar_button_5.grid(row=5, column=0, pady=5) 
        self.sidebar_button_6 = customtkinter.CTkButton(self.sidebar_frame, text="Destroy all squares", command=self.destroy_all_square)
        self.sidebar_button_6.grid(row=6, column=0, pady=5) 



        self.checkbox_1 = customtkinter.CTkCheckBox(self.sidebar_frame, text="Rescale square with image")
        self.checkbox_1.grid(row=7, column=0, padx=(30,0), pady=5 ,sticky="nw")
        self.checkbox_1.select()
        self.checkbox_2 = customtkinter.CTkCheckBox(self.sidebar_frame, text="Something 1")
        self.checkbox_2.grid(row=8, column=0, padx=(30,0), pady=5,sticky="nw")
        self.checkbox_2.select()
        self.checkbox_3 = customtkinter.CTkCheckBox(self.sidebar_frame, text="Something 2")
        self.checkbox_3.grid(row=9, column=0, padx=(30,0), pady=5,sticky="nw")
        self.checkbox_3.select()

        self.checkbox_slider_frame = customtkinter.CTkFrame(self.sidebar_frame)
        self.checkbox_slider_frame.grid(row=10, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.canvas = customtkinter.CTkCanvas(self, height=1000, bg="white")
        self.canvas.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.canvas.bind("<MouseWheel>", self.zoom_event)
        self.squares = []
        self.zoom_factor = 0.2
        self.zoom_label = customtkinter.CTkLabel(self.sidebar_frame, text=f"Zoom Level: {self.zoom_factor*100}%", font=customtkinter.CTkFont(size=12))
        self.zoom_label.grid(row=11, column=0, padx=20, pady=(20, 10))


    def on_double_click_create_app_boxes(self,square): 
        self.old_width = square.width
        self.old_height = square.height

        self.edit_width_slider_text = customtkinter.CTkLabel(self.sidebar_frame, text=f"Width: {square.width}", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.edit_width_slider_text.grid(row=6, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.edit_width_slider = customtkinter.CTkSlider(self.sidebar_frame,from_=0, to=1, number_of_steps=20, command=lambda value: self.change_square_size(square,"width"))
        self.edit_width_slider.grid(row=7, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.edit_width_slider_text.bind("<Double-Button-1>", command=lambda value: self.change_square_size_precisely(square,"width"))

        self.edit_height_slider_text = customtkinter.CTkLabel(self.sidebar_frame, text=f"Height: {square.height}", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.edit_height_slider_text.grid(row=8, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.edit_height_slider = customtkinter.CTkSlider(self.sidebar_frame,from_=0, to=1, number_of_steps=20,  command=lambda value: self.change_square_size(square,"height"))
        self.edit_height_slider.grid(row=9, column=0, padx=(20, 10), pady=(10, 10), sticky="ew") 
        self.edit_height_slider_text.bind("<Double-Button-1>", command=lambda value: self.change_square_size_precisely(square,"height"))

        self.edit_size_slider_text = customtkinter.CTkLabel(self.sidebar_frame, text=f"Both: {square.width}x{square.height}", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.edit_size_slider_text.grid(row=10, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.edit_size_slider = customtkinter.CTkSlider(self.sidebar_frame,from_=0, to=1, number_of_steps=20,  command=lambda value: self.change_square_size(square,"both"))
        self.edit_size_slider.grid(row=11, column=0, padx=(20, 10), pady=(10, 10), sticky="ew") 
        self.edit_size_slider_text.bind("<Double-Button-1>", command=lambda value: self.change_square_size_precisely(square,"both"))


    #TO CHANGEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    def change_square_size_precisely(self,square,scalling):
        if(scalling == "width"):
            popup_window = tkinter.Tk()
            popup_window.title("Precise Size Edit")
            popup_window.geometry("300x200")
            def save_changes():
                try:
                    new_width = float(entry.get())
                    if new_width >= 0:
                        square.width = new_width
                        popup_window.destroy()
                    else:
                        raise ValueError("Width must be a non-negative number.")
                except ValueError as e:
                    tkinter.messagebox.showerror("Error", str(e))
            label = tkinter.Label(popup_window, text="Enter new width:")
            label.pack(pady=10)
            entry = tkinter.Entry(popup_window)
            entry.pack(pady=5)
            button = tkinter.Button(popup_window, text="Save", command=save_changes)
            button.pack(pady=10)
            popup_window.mainloop()
            

        if(scalling == "height"):
            popup_window = tkinter.Tk()
            popup_window.title("Precise Size Edit")
            popup_window.geometry("300x200")
            def save_changes():
                try:
                    new_height = float(entry.get())
                    if new_height >= 0:
                        square.height = new_height
                        popup_window.destroy()
                    else:
                        raise ValueError("Width must be a non-negative number.")
                except ValueError as e:
                    tkinter.messagebox.showerror("Error", str(e))
            label = tkinter.Label(popup_window, text="Enter new width:")
            label.pack(pady=10)
            entry = tkinter.Entry(popup_window)
            entry.pack(pady=5)
            button = tkinter.Button(popup_window, text="Save", command=save_changes)
            button.pack(pady=10)
            popup_window.mainloop()


        if(scalling == "both"):
            square.width = int(self.edit_size_slider.get() * (self.old_width+self.old_width))
            square.height = int(self.edit_size_slider.get() * (self.old_height+self.old_height))
            self.edit_size_slider_text.configure(text=f"Both: {square.width}x{square.height}")
        square.update()


    def change_square_size(self,square,scalling):
        if(scalling == "width"):
            square.width = int(self.edit_width_slider.get() * (self.old_width+self.old_width))
            self.edit_width_slider_text.configure(text=f"Width: {square.width}")
        if(scalling == "height"):
            square.height = int(self.edit_height_slider.get() * (self.old_height+self.old_height))
            self.edit_height_slider_text.configure(text=f"Height: {square.height}")
        if(scalling == "both"):
            square.width = int(self.edit_size_slider.get() * (self.old_width+self.old_width))
            square.height = int(self.edit_size_slider.get() * (self.old_height+self.old_height))
            self.edit_size_slider_text.configure(text=f"Both: {square.width}x{square.height}")
        square.update()


    def show_square_data(self, square):
        self.square_data_label.configure(text=f"Selected Square: Width: {square.width}, Height: {square.height}")


    def update_square_label(self, square):
        self.show_square_data(square)


    def getting_image_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.image = Image.open(file_path)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.image_item = self.canvas.create_image(0, 0, anchor=customtkinter.NW, image=self.image_tk)
            self.canvas.lower(self.image_item)
            self.apply_zoom_img()


    def zoom_event(self, event):
        if event.delta > 0: self.zoom_factor *= 1.2
        else: self.zoom_factor /= 1.2
        self.apply_zoom_img()
        self.apply_zoom_square()


    def apply_zoom_square(self):
        if(self.checkbox_1.get()):
            for square in self.squares:
                square.change_zoom_factor(self.zoom_factor)


    def apply_zoom_img(self):
        try:
            if self.image_item is not None:
                width = int(self.image.width * self.zoom_factor)
                height = int(self.image.height * self.zoom_factor)
                resized_image = self.image.resize((width, height), Image.ANTIALIAS)
                self.image_tk = ImageTk.PhotoImage(resized_image)
                self.canvas.itemconfig(self.image_item, image=self.image_tk)
                self.canvas.config(scrollregion=self.canvas.bbox("all"))
                zoom_percentage = int(self.zoom_factor * 100)
                self.zoom_label.configure(text=f"Zoom Level: {zoom_percentage}%",text_color='white')
        except AttributeError:
            zoom_percentage = int(self.zoom_factor * 100)
            self.zoom_label.configure(text=f"Zoom Level: {zoom_percentage}%",text_color='white')


    def getting_screen_data(self):
        import gettingsScreens
        listOfMonitors = gettingsScreens.get_screen_info()
        self.checkboxes = []
        for i, monitors in enumerate(listOfMonitors):
            checkbox_name = f"checkbox_{i+1}"
            checkbox = customtkinter.CTkCheckBox(self.checkbox_slider_frame, text=f"{monitors[1]} : {monitors[2]}x{monitors[3]}")
            checkbox.grid(row=i+3, column=0, pady=(20, 0), padx=20, sticky="n")
            self.checkboxes.append(checkbox)   
            checkbox.configure(command=lambda checkbox=checkbox, name=monitors[1], width=monitors[2], height=monitors[3]: self.create_or_delete_rectangle(checkbox, name, width, height))


    def create_or_delete_rectangle(self,checkbox,name,width,height):
        if checkbox.get():
            square = Square(self.canvas, 10, 10, width, height, color='red', tag=name, zoom_factor=self.zoom_factor)
            self.squares.append(square)
        else: Square.remove(self,tag=name)
    
    def destroy_all_square(self):
        for index, square in enumerate(self.squares):
            square.remove(square.tag)
            Square.remove(self,square.tag)
        for checkbox in self.checkboxes:
            checkbox.deselect()

    def check_overlap(self):
        overlap_images = []
        for i, square in enumerate(self.squares):
            overlap_image = Image.new("RGBA", (int(self.image.width), int(self.image.height)))
            x1 = int(square.x/square.zoom_factor)
            y1 = int(square.y/square.zoom_factor)
            x2 = int(square.width + square.x/square.zoom_factor)
            y2 = int(square.height + square.y/square.zoom_factor)
            img = Image.new("RGBA", (x2, y2), square.color)
            overlap_image.paste(img, (x2, y2), img)

            cropped_image = self.image.crop((x1,y1,x2,y2))
            alpha = overlap_image.split()[3]
            cropped_image.paste(overlap_image, (x2, y2), alpha)
            overlap_images.append(cropped_image)
        return overlap_images


    def save_overlap(self):
        overlap_images = self.check_overlap()
        current_directory = os.getcwd()
        print(current_directory)
        folder_name = "Sliced_Wallpaper"
        folder_path = os.path.join(current_directory, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for i, cropped_image in enumerate(overlap_images):
            file_path = os.path.join(folder_path, f"img{i+1}.png")
            index = 1
            while os.path.exists(file_path):
                file_path = os.path.join(folder_path, f"img{i+1}_{index}.png")
                index += 1
            cropped_image.save(file_path)


    def save_square_locations_to_file(self):
        folder_path = os.path.join(os.getcwd(), "Sliced_Wallpaper")
        file_path = os.path.join(folder_path, "Last_Positions.txt")
        with open(file_path, "w") as file:
            for i, square in enumerate(self.squares):
                file.write(f"{i+1},{square.x},{square.y},{square.width},{square.height}\n")


    def load_square_locations_from_file(self):
        self.destroy_all_square()
        folder_path = os.path.join(os.getcwd(), "Sliced_Wallpaper")
        file_path = os.path.join(folder_path, "Last_Positions.txt")   
        loaded_squares = []
        if not os.path.exists(file_path):
            return loaded_squares
        with open(file_path, "r") as file:
            for line in file:
                tag, x1, y1, x2, y2 = map(float, line.strip().split(","))
                square = Square(self.canvas, x1, y1, x2, y2, color='red', tag=tag, zoom_factor=self.zoom_factor)
                self.squares.append(square)


if __name__ == "__main__":
    app = App()
    app.mainloop()
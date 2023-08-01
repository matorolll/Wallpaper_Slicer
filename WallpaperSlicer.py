import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
from tkinter import filedialog


class MyDialog(tkinter.simpledialog.Dialog):
    def __init__(self, parent, title):
        self.my_username = None
        self.my_password = None
        super().__init__(parent, title)

    def body(self, frame):
        # print(type(frame)) # tkinter.Frame
        self.my_username_label = tkinter.Label(frame, width=25, text="Username")
        self.my_username_label.pack()
        self.my_username_box = tkinter.Entry(frame, width=25)
        self.my_username_box.pack()

        self.my_password_label = tkinter.Label(frame, width=25, text="Password")
        self.my_password_label.pack()
        self.my_password_box = tkinter.Entry(frame, width=25)
        self.my_password_box.pack()
        self.my_password_box['show'] = '*'

        return frame

    def ok_pressed(self):
        # print("ok")
        self.my_username = self.my_username_box.get()
        self.my_password = self.my_password_box.get()
        self.destroy()

    def cancel_pressed(self):
        # print("cancel")
        self.destroy()


    def buttonbox(self):
        self.ok_button = tkinter.Button(self, text='OK', width=5, command=self.ok_pressed)
        self.ok_button.pack(side="left")
        cancel_button = tkinter.Button(self, text='Cancel', width=5, command=self.cancel_pressed)
        cancel_button.pack(side="right")
        self.bind("<Return>", lambda event: self.ok_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())

def mydialog(app):
    dialog = MyDialog(title="Login", parent=app)
    return dialog.my_username, dialog.my_password


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

        self.shape = self.canvas.create_rectangle(x, y, x + (width * zoom_factor) , y + (height * zoom_factor), fill=color, tag=tag)
        self.canvas.tag_bind(self.shape, '<B1-Motion>', self.move)
        self.canvas.tag_bind(self.shape, '<Double-Button-1>', self.on_double_click)



    def update(self):
        self.canvas.coords(self.shape, self.x, self.y, self.x + (self.width * self.zoom_factor), self.y + (self.height * self.zoom_factor))


    def move(self, event):
        dx = (event.x - self.x - (self.width * self.zoom_factor) // 2)
        dy = (event.y - self.y - (self.height * self.zoom_factor) // 2)
        self.canvas.move(self.shape, dx, dy)
        self.x += dx
        self.y += dy

    def remove(self,tag):
       self.canvas.delete( self.canvas.find_withtag(tag))


    def set_zoom_factor(self, zoom_factor):
        self.zoom_factor = zoom_factor
        self.canvas.coords(self.shape, self.x, self.y, self.x + (self.width * zoom_factor),  self.y + (self.height * zoom_factor))


    def on_double_click(self, event):
        app.on_double_click_create_app_boxes(self)


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
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Side panel", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Load screens info", command=self.getting_screen_data)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Load screens image", command=self.getting_image_data)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)       
        
        self.checkbox_0 = customtkinter.CTkCheckBox(self.sidebar_frame, text="Show grid")
        self.checkbox_0.grid(row=3, column=0, pady=(20, 0), padx=20, sticky="n")

        self.checkbox_slider_frame = customtkinter.CTkFrame(self.sidebar_frame)
        self.checkbox_slider_frame.grid(row=4, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.canvas = customtkinter.CTkCanvas(self, height=1000, bg="white")
        self.canvas.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.canvas.bind("<MouseWheel>", self.zoom_event)
        self.squares = []
        self.zoom_factor = .2
        self.zoom_label = customtkinter.CTkLabel(self.sidebar_frame, text=f"Zoom Level: {self.zoom_factor*100}%", font=customtkinter.CTkFont(size=12))
        self.zoom_label.grid(row=5, column=0, padx=20, pady=(20, 10))
      


    def on_double_click_create_app_boxes(self,square): 
        self.old_width = square.width
        self.old_height = square.height

        self.edit_width_slider_text = customtkinter.CTkLabel(self.sidebar_frame, text=f"Width: {square.width}", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.edit_width_slider_text.grid(row=6, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.edit_width_slider = customtkinter.CTkSlider(self.sidebar_frame,from_=0, to=1, number_of_steps=9, command=lambda value: self.change_square_size(square,"width"))
        self.edit_width_slider.grid(row=7, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.edit_height_slider_text = customtkinter.CTkLabel(self.sidebar_frame, text=f"Height: {square.height}", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.edit_height_slider_text.grid(row=8, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.edit_height_slider = customtkinter.CTkSlider(self.sidebar_frame,from_=0, to=1, number_of_steps=4,  command=lambda value: self.change_square_size(square,"height"))
        self.edit_height_slider.grid(row=9, column=0, padx=(20, 10), pady=(10, 10), sticky="ew") 

        self.edit_size_slider_text = customtkinter.CTkLabel(self.sidebar_frame, text=f"Both: {square.width}x{square.height}", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.edit_size_slider_text.grid(row=10, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.edit_size_slider = customtkinter.CTkSlider(self.sidebar_frame,from_=0, to=1, number_of_steps=4,  command=lambda value: self.change_square_size(square,"both"))
        self.edit_size_slider.grid(row=11, column=0, padx=(20, 10), pady=(10, 10), sticky="ew") 


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
        if event.delta > 0:
            self.zoom_factor *= 1.2
        else:
            self.zoom_factor /= 1.2
        self.apply_zoom_img()
        self.apply_zoom_square()

    def apply_zoom_square(self):
        for square in self.squares:
            square.set_zoom_factor(self.zoom_factor)

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
            self.zoom_label.configure(text="Need to choose img first in order to zoom!", font=customtkinter.CTkFont(size=12), text_color='red')

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
        else: 
            Square.remove(self,tag=name)
    


if __name__ == "__main__":
    app = App()
    app.mainloop()
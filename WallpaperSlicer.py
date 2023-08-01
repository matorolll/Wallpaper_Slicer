import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
from tkinter import filedialog



class Square:
    def __init__(self, canvas, x, y, width, height, color, tag):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tag = tag
        self.color = color
        self.zoom_factor = 1.0

        self.shape = self.canvas.create_rectangle(x, y, x + width, y + height, fill=color, tag=tag)
        self.canvas.tag_bind(self.shape, '<B1-Motion>', self.move)

    def move(self, event):
        dx = (event.x - self.x - self.width // 2) / self.zoom_factor
        dy = (event.y - self.y - self.height // 2) / self.zoom_factor
        self.canvas.move(self.shape, dx, dy)
        self.x += dx
        self.y += dy

    def remove(self,tag):
       self.canvas.delete( self.canvas.find_withtag(tag))

    def set_zoom_factor(self, zoom_factor):
        self.zoom_factor = zoom_factor



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Wallpaper Spacer")
        self.geometry(f"{1100}x{580}")

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

        self.canvas = customtkinter.CTkCanvas(self, height=700, bg="white")
        self.canvas.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.canvas.bind("<MouseWheel>", self.zoom_image)


        self.zoom_factor = 1.0  # Initialize the zoom factor
        self.zoom_label = customtkinter.CTkLabel(self.sidebar_frame, text="Zoom Level: 100%", font=customtkinter.CTkFont(size=12))
        self.zoom_label.grid(row=5, column=0, padx=20, pady=(20, 10))


    def getting_image_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.image = Image.open(file_path)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.image_item = self.canvas.create_image(0, 0, anchor=customtkinter.NW, image=self.image_tk)
            self.canvas.lower(self.image_item)
            self.zoom_factor = 1.0

    def zoom_image(self, event):
        if event.delta > 0:
            self.zoom_factor *= 1.2
        else:
            self.zoom_factor /= 1.2

        width = int(self.image.width * self.zoom_factor)
        height = int(self.image.height * self.zoom_factor)
        resized_image = self.image.resize((width, height), Image.ANTIALIAS)
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.image_item, image=self.image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
        zoom_percentage = int(self.zoom_factor * 100)
        self.zoom_label.configure(text=f"Zoom Level: {zoom_percentage}%")



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
            square = Square(self.canvas, 10, 10, width*self.zoom_factor, height*self.zoom_factor, color='red', tag=name)
            #self.squares.append(square)
        else: 
            Square.remove(self,tag=name)
    


if __name__ == "__main__":
    app = App()
    app.mainloop()
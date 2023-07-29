import tkinter
import tkinter.messagebox
import customtkinter


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
        
        self.checkbox_slider_frame = customtkinter.CTkFrame(self.sidebar_frame)
        self.checkbox_slider_frame.grid(row=2, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.checkbox_0 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Show grid")
        self.checkbox_0.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")

        self.canvas = customtkinter.CTkCanvas(self, height=700, bg="white")
        self.canvas.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.place_300x300_block(self)



    def getting_screen_data(self):
        import gettingsScreens
        listOfMonitors = gettingsScreens.get_screen_info()

        self.checkboxes = []
        for i, monitors in enumerate(listOfMonitors):
            checkbox_name = f"checkbox_{i+1}"
            checkbox = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text=f"{monitors[1]} : {monitors[2]}x{monitors[3]}")
            checkbox.grid(row=i+3, column=0, pady=(20, 0), padx=20, sticky="n")
            self.checkboxes.append(checkbox)   
            checkbox.configure(command=lambda name=checkbox_name: self.checkbox_checked(name))

    @staticmethod
    def checkbox_checked(checkbox_name):
        print(f"Naciśnięto checkboxa o nazwie: {checkbox_name}")
   
    @staticmethod
    def place_300x300_block(self):
        self.canvas.create_rectangle(0, 0, 300, 300, fill='blue')



if __name__ == "__main__":
    app = App()
    app.mainloop()
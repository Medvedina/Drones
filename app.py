import customtkinter as ctk
from PIL import Image
import pyautogui
import threading
import time

test_dict = []
test_dict.append(dict(id=1, name='Cetus X', description = 'Ахуенный вообщем дрон, летает заебато и камера классная.', type='Ебический', 
                 characteristics = dict(speed = 'дохуя', size = 'оптимальный'), img = Image.open('Images/Cetus.jpg')))
test_dict.append(dict(id=2, name='Shepus XXL', description = 'Хуйня, не работает', type='Жирокоптер', 
                 characteristics = dict(speed = '0', size = 'infinite'), img = Image.open('Images/shepiy.jpg')))
print(test_dict)
class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode('dark')
        #self.width, self.height = pyautogui.size()
        self.state('zoomed')
        self.title('DroneGuide')
        self.geometry(f"{1920}x{1080}")
        self.resizable(width=True, height=True)

        self.filter_flag = False
        self.checkbox_list = []
        self.drones_linst = []

        self.menu_frame = List_Frame(self, title="Квудрокуптеры")
        self.menu_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        
        self.content_frame = ctk.CTkScrollableFrame(self, label_text='DroneHelper')
        self.content_frame.grid(row=0, column=1, pady=(10, 0), sticky='n')
        
        self.search_entry = ctk.CTkEntry(self.content_frame, width=1190)
        self.search_entry.grid(row=0, column=0, padx=(10, 0), sticky='n')
        self.content_frame.configure(width=1340, height=1200)
        
        self.filter_image = ctk.CTkImage(light_image=Image.open('Images/light_filter.png'))
        self.filter_button = ctk.CTkButton(self.content_frame, text='', width=35, image=self.filter_image, command=self.filter)
        self.filter_button.grid(row=0, column=2, padx=(5,0))

        #self.search_image = ctk.CTkImage(text='П')
        self.search_button = ctk.CTkButton(self.content_frame, text='П', width=35)
        self.search_button.grid(row=0, column=1, padx=(5,0))

        self.settings_button = ctk.CTkButton(self.content_frame, text='Н', width=35)
        self.settings_button.grid(row=0, column=3, padx=(5,0))

        self.deploy_drones()

        self.background_geometry = threading.Thread(target=self.dynamic_geometry)
        self.background_geometry.start()

    def dynamic_geometry(self):
        current_geometry = self.geometry()
        while True:
            time.sleep(0.01)
            if current_geometry != self.geometry() or self.content_frame.winfo_width != self.winfo_width()*(1200/1920):
                if self.filter_flag:
                    new_width = self.winfo_width()
                    new_height = self.winfo_height()

                    if new_width < 1600:
                        if self.apply_button.grid_info()['row'] != self.switch.grid_info()['row']+7:
                            self.apply_button.grid_forget()
                            self.apply_button.grid(row=self.switch.grid_info()['row']+7, column=0, pady=(10, 0), sticky='nw')
                    else:
                        if self.apply_button.grid_info()['row'] == self.switch.grid_info()['row']+7:
                            self.apply_button.grid_forget()
                            self.apply_button.grid(row=self.switch.grid_info()['row']+6, column=0, pady=(10, 0), padx=(180, 0), sticky='nw')

                    self.filter_frame.configure(width=new_width*(300/1920), height=new_height*(900/1080))
                    self.menu_frame.configure(width=new_width*(300/1920), height=new_height*(900/1080))
                    self.content_frame.configure(width=new_width*(1200/1920), height=new_height*(900/1080))
                    self.search_entry.configure(width=self.content_frame.winfo_width()-150)

                    current_geometry = self.geometry()
                
                else:
                    new_width = self.winfo_width()
                    new_height = self.winfo_height()
                    self.menu_frame.configure(width=new_width*(300/1920), height=new_height*(900/1080))
                    self.content_frame.configure(width=new_width*(1340/1920), height=new_height*(900/1080))
                    self.search_entry.configure(width=self.content_frame.winfo_width()-150)
                    current_geometry = self.geometry()          

    def switch_event(self, num):
        dictionary_appender = []

        if self.switch_list[num].get() == 'On':
            for checkbox in range(5):
                self.checkbox_var = ctk.StringVar(value='Off')
                self.checkbox_filter = ctk.CTkCheckBox(self.filter_frame, text=f'Подкритерий {checkbox}', variable=self.checkbox_var, 
                                                    onvalue='On', offvalue='Off', command=lambda checkbox=checkbox: self.checkbox_event(checkbox))
                self.checkbox_filter.grid(row=self.switch_list[num].grid_info()['row']+checkbox+1, pady=(2,0), column=0)
                dictionary_appender.append(self.checkbox_filter)
            self.checkbox_list.append(dict(id=num, checkboxes=dictionary_appender, state='Off'))
        else:
            for widget_dict in self.checkbox_list:
                if widget_dict['id'] == num:
                    clear_index = self.checkbox_list.index(widget_dict)
                    for widget in widget_dict['checkboxes']:
                        widget.destroy()
            self.checkbox_list.pop(clear_index)

    def apply_filter(self):
        pass

    def checkbox_event(self, checkbox):
        pass

    def cancel_filter(self):
        for widget in self.filter_frame.winfo_children():
            widget.destroy()

        self.switch_list.clear()
        self.checkbox_list.clear()
        self.filter_frame.grid_forget()
        self.filter_flag = False

    def filter(self):
        try:
            if self.filter_frame.winfo_children():
                self.cancel_filter()
            else:
                raise AttributeError
            
        except AttributeError:
            self.filter_frame = List_Frame(self, title='Фильтр')
            self.filter_frame.grid(row=0, column=2, pady=(10, 0), padx=(10, 0), sticky='ne')
            self.switch_list = []

            for num in range(6):
                self.switch_var = ctk.StringVar(value='On')
                self.switch = ctk.CTkSwitch(self.filter_frame, text=f'Критерий {num}', variable=self.switch_var, 
                                            onvalue='On', offvalue='Off', command=lambda num=num:self.switch_event(num))
                self.switch.grid(row=num*6, column=0, pady=(1, 0), sticky='w')
                self.switch.deselect()
                self.switch_list.append(self.switch)
            
            self.apply_button = ctk.CTkButton(self.filter_frame, text='Применить', command=self.apply_filter, width=100)
            self.apply_button.grid(row=self.switch.grid_info()['row']+6, column=0, pady=(10, 0), padx=(180, 0), sticky='nw')
            self.cancel_button = ctk.CTkButton(self.filter_frame, text='Отмена', command=self.cancel_filter, width=100)
            self.cancel_button.grid(row=self.switch.grid_info()['row']+6, column=0, pady=(10, 0), sticky='nw')
            self.filter_flag = True

    def deploy_drones(self):
        for drone in test_dict:
            self.drone = Drone_Frame(self.menu_frame, drone)
            self.drone.grid(row=drone['id'], column=0, sticky='nw', pady=(5, 0))

class Drone_Frame(ctk.CTkFrame):
    def __init__(self, master, drone):
        super().__init__(master)
        self.drone_image = ctk.CTkImage(dark_image=drone['img'], size=(69, 69))
        self.image_label = ctk.CTkLabel(self, image=self.drone_image, text="")
        self.image_label.grid(row=drone['id'], column=0, sticky='nw')
        self.drone_button = ctk.CTkButton(self, text=f'{drone['name']}')
        self.drone_button.grid(row=drone['id'], column=1, sticky='n')
        self.drone_description = ctk.CTkLabel(self, text=drone['type'])
        self.drone_description.grid(row=drone['id'], column=1, sticky='nw', pady=(30, 0), padx=(5, 0))

class List_Frame(ctk.CTkScrollableFrame):
    def __init__(self, master, title, values=None):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        self.configure(height=750, width=300)

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
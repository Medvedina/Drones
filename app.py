import customtkinter as ctk
from PIL import Image
import pyautogui
import threading
import time
import ctypes
from sys import exit

test_dict = []
test_dict.append(dict(id=1, name='Cetus X', description = 'Ахуенный вообщем дрон, летает заебато и камера классная.', type='Ебический', 
                 characteristics = {'Скорость': 'дохуя', 'Размер': 'оптимальный', 'Камера': 'Ахуенная'}, img = Image.open('Images/Cetus.jpg'), images = [Image.open('Images/Cetus.jpg'), Image.open('Images/shepiy.jpg')]))
test_dict.append(dict(id=2, name='Shepus XXL', description = 'Разработан каширскими инженерами в эпоху жиросотворения. Дрон является моделью повышенного веса, пониженной скорости, и вообще пониженного всего. Я хуй знает нахуя он такой нужон и мне нужно забить описание побольше для теста, так что вот ебать его рот такой вот дронище', type='Жирокоптер', 
                 characteristics = {'Скорость': '0', 
                                    'Размер': 'infinite', 
                                    'Камера': 'Слепой нахуй =(', 
                                    'Масса': 'Сломал весы', 
                                    'Подбородки': '4 насчитал', 
                                    'Потребление': 'Кормить не успеваю, да и сам есть тоже',
                                    'Польза': 'Общак'}, img = Image.open('Images/shepiy.jpg'), images = [Image.open('Images/shepiy.jpg'), Image.open('Images/Shep2.jpg')]))
print(test_dict)

def get_scale_factor():
    try:
        hdc = ctypes.windll.user32.GetDC(0)
        dpi_x = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)
        scale_factor = dpi_x / 96
        ctypes.windll.user32.ReleaseDC(0, hdc)
        print(scale_factor)
        return scale_factor

    except Exception as e:
        raise e

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.scale_factor = get_scale_factor()
        ctk.set_appearance_mode('dark')
        self.width, self.height = pyautogui.size()
        self.state('zoomed')
        self.title('DroneGuide')
        self.geometry(f"{self.width}x{self.height}")
        ctk.set_widget_scaling(1 / self.scale_factor)
        ctk.set_window_scaling(1 / self.scale_factor)
        self.resizable(width=True, height=True)

        self.filter_flag = False
        self.checkbox_list = []
        self.drones_list = []
        self.current_drone = []
        self.background_flag = True

        self.menu_frame = ListFrame(self, title="Квудрокуптеры")
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
        while self.background_flag:
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
        return 0
    
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
            self.filter_frame = ListFrame(self, title='Фильтр')
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
            self.drone = DroneFrame(self.menu_frame, drone, self)
            self.drone.grid(row=drone['id'], column=0, sticky='nw', pady=(5, 0))

    def open_drone(self, id):
        for drone in test_dict:
            if drone['id'] == id:
                for widget in self.current_drone:
                    widget.destroy()
                self.drone_frame = ctk.CTkFrame(master=self.content_frame)
                self.drone_frame.grid_rowconfigure((0,1,2,3), weight=1)
                self.drone_frame.grid_columnconfigure((0,1,2,3), weight=1)
                self.drone_frame.configure(width=1200)
                self.drone_frame.grid(row=1, column=0, sticky='nsew', columnspan=3)
                name = drone['name']
                description = drone['description']
                type = drone['type']
                characteristics = drone['characteristics']
                images = drone['images']
                self.images_tab = ImagesTab(master=self.drone_frame, images=images)
                self.drone_descripiton = DroneDescription(master=self.drone_frame, name=name, type=type, characteristics=characteristics, description=description)
                self.images_tab.grid(row=0, column=0, sticky='w', padx=10, rowspan=self.drone_descripiton.counter+4)
                self.current_drone = [self.images_tab, self.drone_frame]
                for widget in self.drone_descripiton.widget_list:
                    self.current_drone.append(widget)
 
class ImagesTab(ctk.CTkTabview):
    def __init__(self, master, images):
        super().__init__(master)
        print(master)
        for i in range(len(images)):
            self.add(f'Фото {i+1}')
            self.image = ctk.CTkImage(dark_image=images[i], size=(500, 500))
            self.image_label = ctk.CTkLabel(self.tab(f'Фото {i+1}'), image=self.image, text='')
            self.image_label.pack(side='top')

class DroneDescription:
    def __init__(self, master, name, type, characteristics:dict, description):
        print(master)
        self.widget_list = []
        self.counter = 0
        self.name_label = ctk.CTkLabel(master, text=name, font=('Arial', 50, 'bold'))
        self.name_label.grid(column=1, row=1, sticky='n', padx=20, pady=(10, 0))
        self.widget_list.append(self.name_label)
        self.type_label = ctk.CTkLabel(master, text=type, font=('Arial', 50, 'bold'))
        self.type_label.grid(column=1, row=2, sticky='n', padx=20, pady=(0, 100))
        self.widget_list.append(self.type_label)
        self.title_label = ctk.CTkLabel(master, text='Характеристики', font=('Arial', 30, 'bold'))
        self.title_label.grid(column=1, row=3, sticky='nw', pady=(0, 40))
        for key, value in characteristics.items():
            self.counter += 1
            self.char_label = ctk.CTkLabel(master, text=f'{key}: {value}', font=('Arial', 20, 'bold'))
            self.char_label.grid(column=1, row=3+self.counter, sticky='nw', pady=(0, 0))
        self.description_textbox = ctk.CTkTextbox(master, width=1100, font=('Arial', 20, 'bold'), wrap='word')
        self.description_textbox.grid(row=4+self.counter, column=0, sticky='ew', columnspan=2, padx=10, pady=(10, 0))
        self.description_textbox.insert("0.0", description)
        self.description_textbox.configure(state=ctk.DISABLED)
                 
class DroneFrame(ctk.CTkFrame):
    def __init__(self, master, drone, window):
        super().__init__(master)
        self.drone_image = ctk.CTkImage(dark_image=drone['img'], size=(69, 69))
        self.image_label = ctk.CTkLabel(self, image=self.drone_image, text="")
        self.image_label.grid(row=drone['id'], column=0, sticky='nw')
        self.drone_button = ctk.CTkButton(self, text=f'{drone['name']}', command=lambda i=drone['id']:window.open_drone(i))
        self.drone_button.grid(row=drone['id'], column=1, sticky='n')
        self.drone_description = ctk.CTkLabel(self, text=drone['type'])
        self.drone_description.grid(row=drone['id'], column=1, sticky='nw', pady=(30, 0), padx=(5, 0))
        

class ListFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, title, values=None):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        self.configure(height=750, width=300)

if __name__ == '__main__':
    app = MainWindow()

    def on_closing():
        app.background_flag = False
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
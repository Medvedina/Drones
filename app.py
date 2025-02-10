import customtkinter as ctk
from PIL import Image
import pyautogui
from tkinter import filedialog

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        #self.width, self.height = pyautogui.size()
        self.state('zoomed')
        self.title('DroneGuide')
        self.geometry(f"{1920}x{1080}")
        self.resizable(width=True, height=True)

        self.canvas = ctk.CTkCanvas(self, bg='white')
        self.canvas.grid(row=0, column=0, sticky='nsew')

        # Создаем прокрутку
        self.scrollbar = ctk.CTkScrollbar(self, orientation='vertical', command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        self.checkbox_list = []
        values = ["value 1", "value 2", "value 3", "value 4", "value 5", "value 6", "value 1", "value 2", "value 3", "value 4", "value 5", "value 6", "value 1", "value 2", "value 3", "value 4", "value 5", "value 6", "value 1", "value 2", "value 3", "value 4", "value 5", "value 6", "value 1", "value 2", "value 3", "value 4", "value 5", "value 6",]

        self.menu_frame = List_Frame(self.canvas, title="Квудрокуптеры", values=values)
        self.menu_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        
        self.content_frame = ctk.CTkScrollableFrame(self.canvas)
        self.content_frame.grid(row=0, column=1, pady=(10, 0), sticky='n')
        
        self.search_entry = ctk.CTkEntry(self.content_frame, width=1200)
        self.search_entry.grid(row=0, column=0, padx=(10, 0), sticky='n')
        self.content_frame.configure(width=1340, height=900)
        
        self.filter_image = ctk.CTkImage(light_image=Image.open('C:/Users/Sergey/Desktop/Drones/Images/light_filter.png'))
        self.filter_button = ctk.CTkButton(self.content_frame, image=self.filter_image, text='', width=25, command=self.filter)
        self.filter_button.grid(row=0, column=2, padx=(5,0))
        #self.search_image = ctk.CTkImage(text='П')
        self.search_button = ctk.CTkButton(self.content_frame, text='П', width=35)
        self.search_button.grid(row=0, column=1, padx=(5,0))
        self.settings_button = ctk.CTkButton(self.content_frame, text='Н', width=35)
        self.settings_button.grid(row=0, column=3, padx=(5,0))
        self.content_frame.bind('<Configure>', self.on_frame_configure)

        # Настраиваем канвас, чтобы использовать scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor='nw')

        # Делаем сетку растягиваемой
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def on_frame_configure(self, event):
        # Обновляем область канваса, чтобы соответствовать размеру content_frame
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def switch_event(self, num):
        dictionary_appender = []
        if self.switch_list[num].get() == 'On':
            for checkbox in range(5):
                self.checkbox_var = ctk.StringVar(value='Off')
                self.checkbox_filter = ctk.CTkCheckBox(self.filter_frame, text=f'Подкритерий {checkbox}', variable=self.checkbox_var, 
                                                    onvalue='On', offvalue='Off', command=lambda checkbox=checkbox: self.checkbox_event(checkbox))
                self.checkbox_filter.grid(row=self.switch_list[num].grid_info()['row']+checkbox+1, pady=(2,0), column=0)
                dictionary_appender.append(self.checkbox_filter)
            self.checkbox_list.append(dict(id=num, checkboxes=dictionary_appender))
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
        self.content_frame.configure(width=1340, height=900)
        self.search_entry.configure(width=1200)

    def filter(self):
        try:
            if self.filter_frame.winfo_children():
                self.cancel_filter()
            else:
                raise AttributeError
            
        except AttributeError:
            self.content_frame.configure(width=1200)
            self.filter_frame = List_Frame(self, title='Фильтр')
            self.filter_frame.grid(row=0, column=2, pady=(10, 0), padx=(10, 0), sticky='ne')
            self.search_entry.configure(width=1050)
            self.switch_list = []

            for num in range(6):
                self.switch_var = ctk.StringVar(value='On')
                self.switch = ctk.CTkSwitch(self.filter_frame, text=f'Критерий {num}', variable=self.switch_var, 
                                            onvalue='On', offvalue='Off', command=lambda num=num:self.switch_event(num))
                self.switch.grid(row=num*6, column=0, pady=(1, 0), sticky='w')
                self.switch.deselect()
                self.switch_list.append(self.switch)
            
            self.apply_button = ctk.CTkButton(self.filter_frame, text='Применить', command=self.apply_filter, width=100)
            self.apply_button.grid(row=self.switch.grid_info()['row']+6, column=1, pady=(10, 0), sticky='nw')
            self.cancel_button = ctk.CTkButton(self.filter_frame, text='Отмена', command=self.cancel_filter, width=100)
            self.cancel_button.grid(row=self.switch.grid_info()['row']+6, column=0, pady=(10, 0), sticky='nw')
        


class List_Frame(ctk.CTkScrollableFrame):
    def __init__(self, master, title, values=None):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.configure(height=800, width=300)

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
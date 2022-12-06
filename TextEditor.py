# TextEditor.py — программа для редактирования текстовых файлов
# pip install ctypes, keyboard, py_win_keyboard_layout

import ctypes
import sys,os
from tkinter import *
from tkinter import messagebox, Tk, Text, Entry
from tkinter import filedialog, font
from re import findall, sub
from keyboard import press_and_release
from py_win_keyboard_layout import change_foreground_window_keyboard_layout
from Fonts import fonts, view_colors

# Путь и имя файла
file_name = 'Untitled'
file_p = 'None'

# Основа приложения
root = Tk()
root.title(f"Текстовый редактор | Текущий файл — {file_name}")
root.geometry('1200x710')
root.iconbitmap(f"{os.path.dirname(__file__)}\\Redactor.ico")
main_menu = Menu(root)


# Функция изменяет тему
def chenge_theme(theme):
    text_fild['bg'] = view_colors[theme]['text_bg']
    text_fild['fg'] = view_colors[theme]['text_fg']
    text_fild['insertbackground'] = view_colors[theme]['cursor']
    text_fild['selectbackground'] = view_colors[theme]['select_bg']


# Функция изменяет шрифт
def chenge_fonts(fontss):
    text_fild['font'] = fonts[fontss]['font']
    text_new = text_fild['font']


# Функция выходит из приложеия
def notepad_exit(event=None):
    answer = messagebox.askokcancel('Выход', 'Вы точно хотите выйти?')
    if answer:
        root.quit()


# Смена раскладки
def change_lang_keyboard(event=None):
    u = ctypes.windll.LoadLibrary("user32.dll")
    pf = getattr(u, "GetKeyboardLayout")
    if hex(pf(0)) == '0x4190419':
        change_foreground_window_keyboard_layout(0x4090409)
        return True
    else:
        change_foreground_window_keyboard_layout(0x4190419)
        return True


# Сочетания клавиш ctrl + key
def ctrl_key_pressed(event):
    # change_foreground_window_keyboard_layout(0x4090409)
    if event.keycode == 86 and event.keysym != 'v':
        event.widget.event_generate('<<Paste>>')
    elif event.keycode == 67 and event.keysym != 'c':
        event.widget.event_generate('<<Copy>>')
    elif event.keycode == 88 and event.keysym != 'x':
        event.widget.event_generate('<<Cut>>')
    elif event.keycode == 65 and event.keysym != 'a':
        event.widget.event_generate('<<SelectAll>>')
    elif event.keycode == 83 and event.keysym != 's':
        fast_save()
    elif event.keycode == 79 and event.keysym != 'o':
        open_file()
    elif event.keycode == 78 and event.keysym != 'n':
        new_file()
    elif event.keycode == 90 and event.keysym != 'z':
        change_foreground_window_keyboard_layout(0x4090409)
        text_fild.edit_undo
    elif event.keycode == 89 and event.keysym != 'y':
        change_foreground_window_keyboard_layout(0x4090409)
        text_fild.edit_redo
    elif event.keysym == 'equal' or event.keysym == 'minus':
        size = findall(r"\d+",text_fild['font'])
        size_new = size[0]
        if event.keysym == 'minus':
            size_new = int(size[0])-1
        else:
            size_new = int(size[0])+1
        text_fild['font'] = sub(r"(\d+)", str(size_new), text_fild['font'])


def combination(combination):
    if combination == 'Вырезать':
        press_and_release('ctrl+x')
    if combination == 'Увеличить шрифт':
        size = findall(r"\d+", text_fild['font'])
        size_new = int(size[0])+1
        text_fild['font'] = sub(r"(\d+)", str(size_new), text_fild['font'])  
    if combination == 'Уменьшить шрифт':
        size = findall(r"\d+",text_fild['font'])
        size_new = int(size[0])-1
        text_fild['font'] = sub(r"(\d+)", str(size_new), text_fild['font'])
    if combination == 'Вставить':
        press_and_release('ctrl+v')
    if combination == 'Копировать':
        press_and_release('ctrl+c')
    if combination == 'Выделить всё':
        press_and_release('ctrl+a')


# Советы
def recomendation_and_advise():
    messagebox.showinfo('Советы и рекомендации', '1.Использовать комманды \n2.Настройте тему и шрифт удобный вам.\n3.Не забывайте сохранить файл перед закрытием текстового редактора')


def new_file(event=None):
    text_fild.delete('1.0', END)
    root.title("Текстовый редактор | Текущий файл — Untitled")
    return text_fild.get('1.0',END)

# Функция открытия файла
def open_file(event=None):
    file_path = filedialog.askopenfilename(title='Выбор файла', filetypes=(('Текстовые документы (*.txt)', '*.txt'),('Python файлы (*.py)', '*.py'), ('Все файлы', '*.*')))
    if file_path:
        text_fild.delete('1.0', END)
        with open(file_path, encoding='utf8') as f:
            text_fild.insert('1.0', f.read())
        global file_name, file_p
        file_p = file_path
        template = r"\w+\.\w+"
        file_name = findall(template,file_path)
        file_name1 = ""
        for symbol in file_name:
            if symbol == '[' or symbol == "'" or symbol == ']':
                continue
            else:
                file_name1 += symbol
        root.title(f"Текстовый редактор | Текущий файл — {file_name1}") 


# Функция сохранения файла        
def save_file(event=None):
    file_path = filedialog.asksaveasfilename(filetypes=(('Текстовые документы (*.txt)', '*.txt'),('Python файлы (*.py)', '*.py'),('Все файлы', '*.*'))) 
    try:
        f = open(file_path, 'w', encoding='utf-8')
        text = text_fild.get('1.0', END)
        f.write(text)
        global file_name, file_p
        file_p = file_path
        template = r"\w+\.\w+"
        file_name = findall(template, file_path)
        file_name1 = ""
        for symbol in file_name:
            if symbol == '[' or symbol == "'" or symbol == ']':
                continue
            else:
                file_name1 += symbol
        root.title(f"Текстовый редактор | Текущий файл — {file_name1}")
        f.close()
    except FileNotFoundError:
        pass


#Быстрое сохранение
def fast_save(event=None):
    file_path = file_p
    if file_path not in ["Untitled", None, '']:
        with open(file_path, 'w', encoding='utf-8') as f:
            text = text_fild.get('1.0', END)
            f.write(text)


# Функция вывода информации о программе   
def about_program():
    pv = findall(r"\d+\.\d+\.+\d ",sys.version)
    pversion = "3.10.6 "
    messagebox.showinfo(title='ПC "Текстовый редактор"', message=f'Версия: 1.0\nАвтор: Плакхин Даниил\nOC: {sys.platform}\nПрограмма была написана на Python{pversion} ')


# Документация
def documentaion():
    # TODO сделать окно или ссылку на документацию
    doc = Tk()


# Bold text
def bold_it():
    bold_font = font.Font(text_fild, text_fild.cget("font"))
    bold_font.configure(weight="bold")
    text_fild.tag_configure("bold", font=bold_font)
    try:
        current_tags = text_fild.tag_names("sel.first")
    except Exception:
        current_tags = "No"
    if current_tags != "No":
        if "bold" in current_tags:  
            text_fild.tag_remove("bold","sel.first","sel.last")
        else:
            text_fild.tag_add("bold","sel.first","sel.last")


# Italic text
def italic_it():
    italic_font = font.Font(text_fild, text_fild.cget("font"))
    italic_font.configure(slant="italic")
    text_fild.tag_configure("italic", font=italic_font)
    try:
        current_tags = text_fild.tag_names("sel.first")
    except Exception:
        current_tags = "No"
    if current_tags != "No":
        if "italic" in current_tags:
            text_fild.tag_remove("italic", "sel.first", "sel.last")
        else:
            text_fild.tag_add("italic", "sel.first", "sel.last")


# Правая кнопка мыши
def command_right_click(event):
    command_menu.post(event.x_root, event.y_root)


# Сочетания клавиш
root.bind('<Control-KeyPress>', ctrl_key_pressed)
root.bind('<Control-o>', open_file)
root.bind('<Control-Shift-KeyPress-S>', save_file)
root.bind('<Shift-Alt_L>', change_lang_keyboard)
root.bind('<Control-s>', fast_save)
root.bind('<Button-3>', command_right_click)
root.bind('<Control-n>', new_file)
root.protocol('WM_DELETE_WINDOW', notepad_exit)

# Файл
file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label='Создать', accelerator='Ctrl-N', command=new_file)
file_menu.add_command(label='Открыть', accelerator='Ctrl-O', command=open_file)
file_menu.add_command(label='Сохранить как', accelerator='Ctrl-Shift-S', command=save_file)
file_menu.add_command(label='Cохранить', accelerator='Ctrl-S', command=fast_save)
file_menu.add_separator()
file_menu.add_command(label='Закрыть', accelerator='Alt-F4', command=notepad_exit)
root.config(menu=file_menu)

# Вид
view_menu = Menu(main_menu, tearoff=0)
view_menu_sub = Menu(view_menu, tearoff=0)
font_menu_sub = Menu(view_menu, tearoff=0)   
view_menu_sub.add_command(label='Тёмная', command=lambda: chenge_theme('dark'))
view_menu_sub.add_command(label='Светлая', command=lambda: chenge_theme('light'))
view_menu_sub.add_command(label='Хаос', command=lambda: chenge_theme('dark_blue'))
view_menu_sub.add_command(label='Серая',command=lambda: chenge_theme('gray'))
view_menu.add_cascade(label='Тема', menu=view_menu_sub)
font_menu_sub.add_command(label='Arial', command=lambda: chenge_fonts('Arial'))
font_menu_sub.add_command(label='Comic Sans MS', command=lambda: chenge_fonts('CSMS'))
font_menu_sub.add_command(label='Times New Roman', command=lambda: chenge_fonts('TNR'))
font_menu_sub.add_command(label='Consolas', command=lambda: chenge_fonts('Consolas'))
font_menu_sub.add_command(label='Courier New',command=lambda: chenge_fonts('Courier New'))
font_menu_sub.add_command(label='Colonna MT', command=lambda: chenge_fonts('Colonna MT'))
font_menu_sub.add_command(label='Agency FB',command=lambda: chenge_fonts('Agency FB'))
font_menu_sub.add_command(label='Algerian',command = lambda: chenge_fonts('Algerian'))
font_menu_sub.add_command(label='Red Hat',command = lambda: chenge_fonts('Red Hat'))
font_menu_sub.add_command(label='JetBrains', command = lambda: chenge_fonts('JetBrains'))
font_menu_sub.add_command(label='Calibri',command = lambda: chenge_fonts('Calibri'))
font_menu_sub.add_command(label='Monocraft', command = lambda: chenge_fonts('Monocraft'))
view_menu.add_cascade(label='Шрифт...', menu=font_menu_sub)
root.config(menu=view_menu)

# Справка
help_menu = Menu(main_menu, tearoff =0)
help_menu.add_command(label="О программе", command=about_program)
help_menu.add_command(label="Советы и рекомендации", command =recomendation_and_advise)
help_menu.add_command(label="Документация", command=documentaion)
root.config(menu=help_menu)

#command_menu
command_menu = Menu(main_menu, tearoff=0)
command_menu.add_command(label="Вырезать", accelerator="Ctrl-X", command=lambda: combination("Вырезать"))
command_menu.add_command(label="Увеличить шрифт", accelerator="Ctrl-=", command=lambda:combination('Увеличить шрифт'))
command_menu.add_command(label="Уменьшить шрифт", accelerator="Ctrl-", command=lambda:combination('Уменьшить шрифт'))
command_menu.add_command(label="Вставить", accelerator="Ctrl-V", command=lambda: combination('Вставить'))
command_menu.add_command(label="Копировать",accelerator="Ctrl-C",command=lambda: combination('Копировать'))
command_menu.add_command(label="Выделить всё", accelerator="Ctrl-A", command=lambda:combination('Выделить всё'))
command_menu.add_command(label="Отменить",accelerator="Ctrl-Z",command=lambda:text_fild.edit_undo)
command_menu.add_command(label="Повторить",accelerator="Ctrl-Y",command=lambda:text_fild.edit_redo)
root.config(menu=command_menu)


# Добавление списков меню
main_menu.add_cascade(label='Файл', menu=file_menu)
main_menu.add_cascade(label='Вид', menu=view_menu)
main_menu.add_cascade(label='Cправка', menu=help_menu)
main_menu.add_cascade(label='Комманды',menu=command_menu)
root.config(menu=main_menu)

#Tool bar
tool_bar = Frame(root)
tool_bar.pack(fill = X)

# Текстовое поле (main frame)
f_text = Frame(root)
f_text.pack(fill=BOTH, expand=1)

# Добавление в main frame текстового поля
text_fild = Text(f_text,
                 bg='white',
                 fg='black',
                 padx=10,
                 pady=10,
                 insertbackground='brown',
                 selectbackground='#911122',
                 undo = True,
                 spacing3=10,
                 width=30,
                 font=['Red Hat Mono', 15],
                 wrap = "none"
                 )
text_fild.pack(expand=1, fill=BOTH, side=LEFT)

def undo(event = None):
    text_fild.edit_undo

def redo(event = None):
    text_fild.edit_redo
    
root.bind('<Control-z>',undo)
root.bind('<Control-y>',redo)


# Status bar
status_bar = Label(root,text = "Not saved",anchor=E)
status_bar.pack(fill = X,side = BOTTOM, ipady = 5)

# Меню прокрутки
scroll = Scrollbar(f_text, command = text_fild.yview)
scroll.pack(side=LEFT, fill=Y)
text_fild.config(yscrollcommand=scroll.set)
hor_scroll = Scrollbar(text_fild,command = text_fild.xview, orient = 'horizontal')
hor_scroll.pack(fill=X,side = BOTTOM)
text_fild.config(xscrollcommand=hor_scroll.set)

#Bold Button 
bold_button = Button(tool_bar,text = "Bold",command = bold_it)
bold_button.grid(row = 0,column = 0,sticky = W)

#Italics Button
italic_button = Button(tool_bar,text = "Italic",command = italic_it)
italic_button.grid(row = 0,column = 1,padx = 5)


#Только при запуске из этого файла
if __name__ == '__main__':
    root.mainloop()


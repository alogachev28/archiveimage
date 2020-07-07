import exifread
import os
import shutil
from tkinter import *
import time
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from sortimg import Image
import zipfile
from sortimg import check_img


global dir
dir = ''



def askdir1():
    global dir
    dir = fd.askdirectory(title = 'Выбор папки')
    l2.delete(1.0, END)
    l2.insert(1.0, dir)
    return dir

def choose_date(dir, root1):
    from sortimg import sort_date
    b1 = Button(root1, text='Сортировка по годам', width = 20, height = 1, command = lambda:sort_date(dir, 4, root, root1))
    b2 = Button(root1, text='Сортировка по месяцам', width = 20, height = 1, command = lambda: sort_date(dir, 7, root, root1))
    b3 = Button(root1, text='Сортировка по дням', width = 20, height = 1, command = lambda:sort_date(dir, 10, root, root1))
    b4 = Button(root1, text='Сортировка по часам', width = 20, height = 1, command = lambda:sort_date(dir, 13, root, root1))

    b1.place(x = 10, y = 70)
    b2.place(x=10, y=100)
    b3.place(x=10, y=130)
    b4.place(x=10, y=160)


def asksort():
    global dir
    dir = check_dir(dir)
    root.withdraw()
    root1 = Toplevel()
    root1.geometry('750x250+300+200')
    but1 = Button(root1, text='Каталогизация по дате', width = 23, height = 3, command = lambda:choose_date(dir, root1))
    from sortimg import sort_format
    but2 = Button(root1, text = 'Каталогизация по формату', width = 23, height = 3, command = lambda:sort_format(dir, root, root1))
    from sortimg import sort_ab
    but3 = Button(root1, text='Каталогизация по разрешению', width=23, height=3, command=lambda: sort_ab(dir, root, root1))
    from sortimg import sort_orient
    but4 = Button(root1, text='Каталогизация по ориентации', width=23, height=3, command=lambda: sort_orient(dir, root, root1))
    but1.place(x = 10, y = 10)
    but2.place(x = 190, y = 10)
    but3.place(x = 370, y = 10)
    but4.place(x = 550, y = 10)
    root1.mainloop()

def check_dir(dir):
    if dir == '':
        mb.showerror('Ошибка', 'Папка не выбрана')
        return askdir1()
    return dir


def addimg(dir, img):
    if not os.path.isdir(img):
        dird, named = os.path.split(dir)
        if named == 'Сортировка по формату':
            from sortimg import sort_format_move
            sort_format_move(img, dir)
        elif named == 'Сортировка по годам':
            from sortimg import sort_date_move
            sort_date_move(img, ' годам', 4, dir)
        elif named == 'Сортировка по месяцам':
            from sortimg import sort_date_move
            sort_date_move(img, ' месяцам', 7, dir)
        elif named == 'Сортировка по дням':
            from sortimg import sort_date_move
            sort_date_move(img, ' дням', 10, dir)
        elif named == 'Сортировка по часам':
            from sortimg import sort_date_move
            sort_date_move(img, ' часам', 13, dir)
        elif named == 'Сортировка по разрешению':
            from sortimg import sort_ab_move
            sort_ab_move(img, dir)
        elif named == 'Сортировка по ориентации':
            from sortimg import sort_orient_move
            sort_orient_move(img, dir)
        else:
            diri, namei = os.path.split(img)
            img1 = Image(diri, namei)
            shutil.move(img1.directive + '/' + img1.name, dir)
        mb.showinfo('Добавлено', 'Файл успешно добавлен в каталог')



def addtodir(dir):
    dir = check_dir(dir)
    img = fd.askopenfilename(title = "Выбрать файл")
    if check_img(img) == True:
        addimg(dir, img)
    else:
        mb.showerror('Ошибка','Вы выбрали не фотографию')
        addtodir(dir)

def archive(dir, dir1, n, root, root2, zip):
    for folder, subfolders, files in os.walk(dir):
        for file in files:
            if check_img(file) == True:
                if n == 1:
                    if file.endswith('.jpeg') or file.endswith('.JPEG') or file.endswith('.jpg') or file.endswith('.JPG') or file.endswith('.png') or file.endswith('.PNG'):
                        zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder, file), dir), compress_type=zipfile.ZIP_STORED)
                    else:
                        zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder, file), dir), compress_type=zipfile.ZIP_DEFLATED)
                else:
                    zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder, file), dir), compress_type=zipfile.ZIP_STORED)
    zip.close()
    mb.showinfo('Выполнено', 'Архив успешно создан')
    root2.destroy()
    root.deiconify()

def make_ar(dir, root):
    dir = check_dir(dir)
    dird, named = os.path.split(dir)
    dir1 = fd.askdirectory(title = 'Куда сохранить архив')
    zip = zipfile.ZipFile(dir1 + '/' + named + '.zip', 'w')
    root.withdraw()
    root2 = Toplevel()
    root2.geometry('200x100+300+200')
    but1 = Button(root2, text='С сжатием', width=10, height=3, command = lambda: archive(dir, dir1, 1, root, root2, zip))
    but2 = Button(root2, text='Без сжатия', width=10, height=3, command = lambda: archive(dir, dir1, 0, root, root2, zip))
    but1.place(x=10, y=10)
    but2.place(x=100, y=10)
    root2.mainloop()

















root = Tk()
root.geometry('600x300+200+100')
root.title('Логачев.Курсовая')

mainmenu = Menu(root)
root.config(menu=mainmenu)
filemenu = Menu(mainmenu, tearoff = 0)
filemenu.add_command(label = 'Открыть...', command = askdir1)
filemenu.add_command(label = 'Выход', command = sys.exit)

helpmenu = Menu(mainmenu, tearoff = 0)

mainmenu.add_cascade(label = 'Файл', menu = filemenu)
l1 = Label(text = 'Выбранная директория: ', width = 20)
l2 = Text(width = 72, height = 1)
b1 = Button(root, text='Автоматическая каталогизация', width=25, height=5, command = asksort)
b2 = Button(root, text = 'Добавление в каталог', width = 25, height = 5, command = lambda: addtodir(dir))
b3 = Button(root, text = 'Создание архива', width = 25, height = 5, command = lambda: make_ar(dir, root))


l1.place(x = 5, y = 5)
l2.place(x = 10, y = 25)
b1.place(x = 110, y = 55)
b2.place(x = 110, y = 150)
b3.place(x = 310, y = 55)

root.mainloop()



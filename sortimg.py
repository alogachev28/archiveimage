import os
import time
import shutil
import exifread
from tkinter import messagebox as mb
from PIL import Image as pimg

class Image():

    def __init__(self, directive, name):
        self.directive = directive
        self.name = name

        self.format = str()
        self.cdate = str()
        self.alldir = self.directive + '/' + self.name
        self.a = 0
        self.b = 0
        if not os.path.isdir(self.directive + '/' + self.name):
            self.getformat()
            self.getcdate()
            self.getab()

    def getformat(self):
        xi = -1
        while self.name[xi] != '.' and self.name:
            xi = xi-1
        self.format = self.name[xi:].lower()


    def getcdate(self):
        if self.format.lower() == '.jpg' or self.format.lower() == '.tiff' or self.format.lower() == '.jpeg':
            a = open(self.directive + '/' + self.name, 'rb')
            tags = exifread.process_file(a)
            print(tags)
            if 'Image DateTime' in tags:
                s = str(tags['Image DateTime'])
            else:
                s = '0000.00.00 00.00.00'
        else:
            a1 = time.ctime(os.path.getctime(self.directive +'/'+ self.name))
            s = a1[-4:] + ':'
            if a1[4:7] == 'Jan':
                s = s + '01.'
            elif a1[4:7] == 'Feb':
                s = s + '02.'
            elif a1[4:7] == 'Mar':
                s = s + '04.'
            elif a1[4:7] == 'Apr':
                s = s + '04.'
            elif a1[4:7] == 'May':
                s = s + '05.'
            elif a1[4:7] == 'Jun':
                s = s + '06.'
            elif a1[4:7] == 'Jul':
                s = s + '07.'
            elif a1[4:7] == 'Aug':
                s = s + '08.'
            elif a1[4:7] == 'Sep':
                s = s + '09:'
            elif a1[4:7] == 'Oct':
                s = s + '10:'
            elif a1[4:7] == 'Nov':
                s = s + '11:'
            elif a1[4:7] == 'Dec':
                s = s + '12:'
            s = s + a1[8:10] + ' ' + a1[11:19]
        for i in range(len(s)):
            if s[i] == ':':
                self.cdate = self.cdate + '.'
            else:
                self.cdate = self.cdate + s[i]
    def getab(self):
        im = pimg.open(self.directive + '/' + self.name)
        (self.a, self.b) = im.size
        im.close()

global form
form = ['.jpeg', '.jpg', '.png', '.bmp','.raw','.gif','.ico','.tiff']

def check_img(name):
    xi = -1
    while name[xi] != '.' and name:
        xi = xi - 1
    for i in range(8):
        if name[xi:].lower() == form[i]:
            return True



# -----------------------Сортировка по дате(год-месяц-день-час)--------------------------------
def sort_date(dir, n, root, root1):
    files = os.listdir(dir)
    if n == 4:
        s = ' годам'
    elif n == 7:
        s = ' месяцам'
    elif n == 10:
        s = ' дням'
    elif n == 13:
        s = ' часам'
        
    if not (os.path.exists(dir + '/' + 'Сортировка по' + s)):
        os.mkdir(dir + '/' + 'Сортировка по' + s)
    dir1 = dir + '/' + 'Сортировка по' + s

    for x in files:
        if not os.path.isdir(dir + '/' + x):
            sort_date_move(dir + '/' + x, s, n, dir1)
    mb.showinfo('Выполнено', 'Каталогизация выполнена')
    root1.destroy()
    root.deiconify()

def sort_date_move(img, s, n, dir1):
    diri, namei = os.path.split(img)
    if check_img(namei) == True:
        img1 = Image(diri, namei)
        if os.path.exists(dir1 + '/' + img1.cdate[:n]):
            if not os.path.exists(dir1 + '/' + img1.cdate[:n] + '/' + img1.name):
                shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + img1.cdate[:n])
            else:
                os.remove(img1.directive + '/' + img1.name)
        else:
            os.mkdir(dir1 + '/' + img1.cdate[:n])
            shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + img1.cdate[:n])


# ----------------Сортировка по формату---------------------------------------------------------------------
def sort_format(dir, root, root1):
    files = os.listdir(dir)
    os.chdir(dir)
    if not(os.path.exists(dir + '/' + 'Сортировка по формату')):
        os.mkdir('Сортировка по формату')
    dir1 = dir + '/' + 'Сортировка по формату'
    for x in files:
        if not os.path.isdir(dir + '/' + x):
            sort_format_move(dir + '/' + x, dir1)

    mb.showinfo('Выполнено', 'Каталогизация выполнена')
    root1.destroy()
    root.deiconify()

def sort_format_move(img, dir1):
    diri, namei = os.path.split(img)
    if check_img(namei) == True:
        img1 = Image(diri, namei)
        if img1.format == '.jpg' or img1.format == '.jpeg':
            if os.path.exists(dir1 + '/' + 'JPEG'):
                if not(os.path.exists(dir1 + '/' + 'JPEG' + '/' + img1.name)):
                    shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + 'JPEG')
                else:
                    os.remove(img1.directive + '/' + img1.name)
            else:
                os.mkdir(dir1 + '/' + 'JPEG')
                shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + 'JPEG')

        elif img1.format == '.png':
            if os.path.exists(dir1 + '/' + 'PNG'):
                if not(os.path.exists(dir1 + '/' + 'PNG' + '/' + img1.name)):
                    shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + 'PNG')
                else:
                    os.remove(img1.directive + '/' + img1.name)
            else:
                os.mkdir(dir1 + '/' + 'PNG')
                shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + 'PNG')

        elif img1.format == '.tiff':
            if os.path.exists(dir1 + '/' + 'TIFF'):
                if not(os.path.exists(dir1 + '/' + 'TIFF' + '/' + img1.name)):
                    shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + 'TIFF')
                else:
                    os.remove(img1.directive + '/' + img1.name)
            else:
                os.mkdir(dir1 + '/' + 'TIFF')
                shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + 'TIFF')

        elif img1.format == '.bmp':
            if os.path.exists(dir1 + '/' + 'BMP'):
                if not(os.path.exists(dir1 + '/' + 'BMP' + '/' + img1.name)):
                    shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + 'BMP')
                else:
                    os.remove(img1.directive + '/' + img1.name)
            else:
                os.mkdir(dir1 + '/' + 'BMP')
                shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + 'BMP')

        elif img1.format == '.ico':
            if os.path.exists(dir1 + '/' + 'ICO'):
                if not(os.path.exists(dir1 + '/' + 'ICO' + '/' + img1.name)):
                    shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + 'ICO')
                else:
                    os.remove(img1.directive + '/' + img1.name)
            else:
                os.mkdir(dir1 + '/' + 'ICO')
                shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + 'ICO')
        elif img1.format == '.raw':
            if os.path.exists(dir1 + '/' + 'RAW'):
                if not(os.path.exists(dir1 + '/' + 'RAW' + '/' + img1.name)):
                    shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + 'RAW')
                else:
                    os.remove(img1.directive + '/' + img1.name)
            else:
                os.mkdir(dir1 + '/' + 'RAW')
                shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + 'RAW')

        elif img1.format == '.gif':
            if os.path.exists(dir1 + '/' + 'GIF'):
                if not(os.path.exists(dir1 + '/' + 'GIF' + '/' + img1.name)):
                    shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + 'GIF')
                else:
                    os.remove(img1.directive + '/' + img1.name)
            else:
                os.mkdir(dir1 + '/' + 'GIF')
                shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + 'GIF')

#--------------------Сортировка по разрешению---------------------------------
def sort_ab(dir, root, root1):
    files = os.listdir(dir)
    if not (os.path.exists(dir + '/' + 'Сортировка по разрешению')):
        os.mkdir(dir + '/' + 'Сортировка по разрешению')
    dir1 = dir + '/' + 'Сортировка по разрешению'

    for x in files:
        if not os.path.isdir(dir + '/' + x):
            sort_ab_move(dir + '/' + x, dir1)
    mb.showinfo('Выполнено', 'Каталогизация выполнена')
    root1.destroy()
    root.deiconify()


def sort_ab_move(img, dir1):
    diri, namei = os.path.split(img)
    if check_img(namei) == True:
        img1 = Image(diri, namei)
        if os.path.exists(dir1 + '/' + str(img1.a) + 'x' + str(img1.b)):
            if not os.path.exists(dir1 + '/' + str(img1.a) + 'x' + str(img1.b) + '/' + img1.name):
                shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + str(img1.a) + 'x' + str(img1.b))
            else:
                os.remove(img1.directive + '/' + img1.name)
        else:
            os.mkdir(dir1 + '/' + str(img1.a) + 'x' + str(img1.b))
            shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + str(img1.a) + 'x' + str(img1.b))

#--------------Сортировка по ориентации------------------------------------
def sort_orient(dir, root, root1):
    files = os.listdir(dir)
    if not (os.path.exists(dir + '/' + 'Сортировка по ориентации')):
        os.mkdir(dir + '/' + 'Сортировка по ориентации')
    dir1 = dir + '/' + 'Сортировка по ориентации'

    for x in files:
        if not os.path.isdir(dir + '/' + x):
            sort_orient_move(dir + '/' + x, dir1)
    mb.showinfo('Выполнено', 'Каталогизация выполнена')
    root1.destroy()
    root.deiconify()


def sort_orient_move(img, dir1):
    diri, namei = os.path.split(img)
    if check_img(namei) == True:
        img1 = Image(diri, namei)
        if img1.a>img1.b:
            s = 'Горизонтальная'
        elif img1.a<img1.b:
            s = 'Вертикальная'
        else:
            s = 'Квадратные изображения'

        if os.path.exists(dir1 + '/' + s):
            if not os.path.exists(dir1 + '/' + s + '/' + img1.name):
                shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + s)
            else:
                os.remove(img1.directive + '/' + img1.name)
        else:
            os.mkdir(dir1 + '/' + s)
            shutil.move(img1.directive + '/' + img1.name, dir1 + '/' + s)
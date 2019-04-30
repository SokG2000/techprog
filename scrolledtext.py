# -*- coding: CP1251 -*-
from tkinter import *


#print('PP4E scrolledtext')


class ScrolledText(Frame):
    def __init__(self, parent=None, text='', file=None, w=35, h=25):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=Y) # сделать растягиваемым
        self.makewidgets(w, h)
        self.settext(text, file)
    
    
    def makewidgets(self, w, h):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN, width=w, height=h)
        sbar.config(command=text.yview) # связать sbar и text
        text.config(yscrollcommand=sbar.set) # сдвиг одного = сдвиг другого
        sbar.pack(side=RIGHT, fill=Y) # первым добавлен - посл. обрезан
        text.pack(side=LEFT, expand=YES, fill=Y) # Text обрезается первым
        self.text = text
    

    def insert(self, pos, text, **options):
        self.text.insert(pos, text, **options)
    
    
    def mark_set(self, mark, pos, **options):
        self.text.mark_set(mark, pos, **options)
    
    
    def settext(self, text='', file=None):
        if file:
            text = open(file, 'r').read()
        self.text.delete('1.0', END) # удалить текущий текст
        self.text.insert('1.0', text) # добавить в стр. 1, кол. 0
        self.text.mark_set(INSERT, '1.0') # установить курсор вставки
        self.text.focus() # сэкономить щелчок мышью
    
    
    def gettext(self): # возвращает строку
        return self.text.get('1.0', END+'-1c') # от начала до конца


if __name__ == '__main__':
    root = Tk()
    if len(sys.argv) > 1:
        st = ScrolledText(file=sys.argv[1]) # имя файла в командной строке
    else:
        st = ScrolledText(text='Words\ngo here') # иначе: две строки
    def show(event):
        print(repr(st.gettext())) # вывести как простую строку
        st.insert(END, 'word\n')
    root.bind('<Key-Escape>', show) # esc = выводит дамп текста
    #root.bind('<Key-Shift>', f) # esc = выводит дамп текста
    root.mainloop()    


if __name__ == '__main__':
    widget = ScrolledList(None, text='Hello widget world')
    widget.pack()
    widget.mainloop()

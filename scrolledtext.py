# -*- coding: CP1251 -*-
from tkinter import *


#print('PP4E scrolledtext')


class ScrolledText(Frame):
    def __init__(self, parent=None, text='', file=None, w=35, h=25):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=Y) # ������� �������������
        self.makewidgets(w, h)
        self.settext(text, file)
    
    
    def makewidgets(self, w, h):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN, width=w, height=h)
        sbar.config(command=text.yview) # ������� sbar � text
        text.config(yscrollcommand=sbar.set) # ����� ������ = ����� �������
        sbar.pack(side=RIGHT, fill=Y) # ������ �������� - ����. �������
        text.pack(side=LEFT, expand=YES, fill=Y) # Text ���������� ������
        self.text = text
    

    def insert(self, pos, text, **options):
        self.text.insert(pos, text, **options)
    
    
    def mark_set(self, mark, pos, **options):
        self.text.mark_set(mark, pos, **options)
    
    
    def settext(self, text='', file=None):
        if file:
            text = open(file, 'r').read()
        self.text.delete('1.0', END) # ������� ������� �����
        self.text.insert('1.0', text) # �������� � ���. 1, ���. 0
        self.text.mark_set(INSERT, '1.0') # ���������� ������ �������
        self.text.focus() # ���������� ������ �����
    
    
    def gettext(self): # ���������� ������
        return self.text.get('1.0', END+'-1c') # �� ������ �� �����


if __name__ == '__main__':
    root = Tk()
    if len(sys.argv) > 1:
        st = ScrolledText(file=sys.argv[1]) # ��� ����� � ��������� ������
    else:
        st = ScrolledText(text='Words\ngo here') # �����: ��� ������
    def show(event):
        print(repr(st.gettext())) # ������� ��� ������� ������
        st.insert(END, 'word\n')
    root.bind('<Key-Escape>', show) # esc = ������� ���� ������
    #root.bind('<Key-Shift>', f) # esc = ������� ���� ������
    root.mainloop()    


if __name__ == '__main__':
    widget = ScrolledList(None, text='Hello widget world')
    widget.pack()
    widget.mainloop()

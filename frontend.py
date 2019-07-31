from tkinter import *
from tkinter import simpledialog
from tkinter.messagebox import *
import backend
win = Tk()
win.title('CUP考试安排查询')
win.geometry("500x200")

ss = '帮助:\n' \
     '    通过使用如下固定格式的与或表达式进行考试信息搜索：\n' \
     '                课程 & 教师 & 班级\n' \
     '    如果条件不足三个，则默认表达式后置条件缺省。\n' \
     '    ps1: xx&yy，为查找课程名为xx且授课教师为yy的信息。\n' \
     '    ps2: xx&&yy，为查找课程名为xx且班级为yy的信息。\n' \
     '    ps3: xx&yy&zz，为按课程、教师和班级三种条件查找。 '

flag = True


def deal():
    exp = ipt.get()
    if not exp:
        return
    res = backend.search(exp.split('&'))
    new_win = Tk()
    new_win.title('查询结果')
    txt = Text(new_win, width=100, height=30)
    srco = Scrollbar(new_win)
    srco.pack(side=RIGHT, fill=Y)
    txt.pack(side=LEFT, fill=Y)
    srco.config(command=txt.yview)
    txt.config(yscrollcommand=srco.set)
    txt.insert(INSERT, res)
    new_win.mainloop()


def update():
    ss = simpledialog.askstring('下载考试通知文件', '请输入考试安排通知网址')
    if backend.getNewXls(ss):
        showinfo('下载成功', 'XLS考试通知文件下载成功!')
        backend.init()
    else:
        showerror('下载失败', '未能成功下载XLS文件')


def clear_input(event):
    global flag
    if flag:
        ipt.delete(0, END)
        flag = False


lb = Label(win, text=ss, justify='left')
lb.pack()

pre_text = Variable()
ipt = Entry(win, width=50, textvariable=pre_text)
ipt.bind('<Key>', clear_input)
ipt.pack()
pre_text.set('输入搜索表达式:')

op = LabelFrame(win, text='操作', width=100)
op.pack()

bt = Button(op, text='查询', command=deal)
bt.grid(row=0, column=1)

upd = Button(op, text='更换xls文件', command=update)
upd.grid(row=0, column=0)

while not backend.pre_check():
    update()
backend.init()
win.mainloop()

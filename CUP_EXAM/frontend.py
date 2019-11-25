#!/usr/bin/env python3
from tkinter import *
from tkinter import simpledialog
from tkinter.messagebox import *
from CUP_EXAM import backend

win = Tk()
win.title('CUP考试安排查询')
win.geometry("400x150")
pre_text = Variable()
ipt = Entry(win, width=40, textvariable=pre_text)

ss = '帮助:\n' \
     '    通过使用如下固定格式的表达式进行考试信息搜索：\n' \
     '          [课程] [教师] [班级]\n' \
     '    []内容可缺省且顺序可变, 但至少输入一个条件。\n'

flag = False
cls_flag = True


def deal():
    exp = ipt.get()
    if not exp:
        return
    rres = backend.search(exp.split())
    new_win = Toplevel()
    new_win.title('查询结果')
    txt = Text(new_win, width=100, height=30)
    srco = Scrollbar(new_win)
    srco.pack(side=RIGHT, fill=Y)
    txt.pack(side=LEFT, fill=Y)
    srco.config(command=txt.yview)
    txt.config(yscrollcommand=srco.set)
    txt.insert(INSERT, rres)
    new_win.mainloop()


def update(url=None, realurl=None):
    if realurl:
        backend.getNewXls(realurl)
        backend.init()
        return
    if not url:
        url = simpledialog.askstring('下载考试通知文件', '请输入考试安排通知网址')
    if backend.getNewXls(url):
        showinfo('下载成功', 'XLS考试通知文件下载成功!')
        backend.init()
    else:
        showerror('下载失败', '未能成功下载XLS文件')


def clear_input(event):
    global cls_flag
    if cls_flag:
        ipt.delete(0, END)
        cls_flag = False
    elif event.char == '\r' or event.char == '\n':
        deal()


def main():
    global flag
    lb = Label(win, text=ss, justify='left')
    lb.pack()
    ipt.bind('<Key>', clear_input)
    ipt.pack()
    pre_text.set('输入搜索表达式:')
    ipt.focus()

    bt = Button(win, text='查询', command=deal)
    bt.pack()

    if not backend.pre_check():
        with open(backend.base_dir + '.last_title', 'w') as f:
            f.write('\n\n')
        flag = True
    res = backend.new_note_check()
    if res == -1:
        showerror('检测文件更新失败', '设备未联网' + ('且无可用考试安排文件，程序自动退出。' if flag else ''))
        if flag:
            exit('No Network')
    elif res:
        if res[-1]:
            if flag:
                ask = True
            else:
                ask = askyesno('发现新的考试安排', '发现新的考试安排:\n    ' + res[1] + '\n\n是否更新考试安排文件?')
            if ask:
                if flag:
                    update(realurl=res[0])
                else:
                    update(url=res[0])
            else:
                backend.init()
        else:
            update('', res[0])
            showinfo('自动更新', '发现考试安排变更，已自动更新。')
    else:
        backend.init()

    win.mainloop()


if __name__ == '__main__':
    main()

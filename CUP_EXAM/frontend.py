#!/usr/bin/env python3
from tkinter import *
from tkinter.messagebox import *
from CUP_EXAM import backend

try:
    win = Tk()
    win.title('CUP考试安排查询')
    win.geometry("400x130")
    pre_text = Variable()
    ipt = Entry(win, width=37, textvariable=pre_text)
except TclError:
    tk_flag = False
    print('Show UI failed! But we provide Basic UI:')
else:
    tk_flag = True

ts = '\n当前考试安排:\n      %s\n'

flag = False
cls_flag = True


def deal():
    exp = ipt.get()
    if not exp:
        return
    rres = backend.search(exp.split())
    if not rres:
        showinfo('暂无相关信息', '无信息，请联系老师查询')
        return
    new_win = Toplevel()
    new_win.title('查询结果')
    txt = Text(new_win, width=100, height=30)
    srco = Scrollbar(new_win)
    srco.pack(side=RIGHT, fill=Y)
    txt.pack(side=LEFT, fill=Y)
    srco.config(command=txt.yview)
    txt.config(yscrollcommand=srco.set)
    txt.insert(INSERT, rres)
    txt.config(state=DISABLED)
    new_win.mainloop()


def update(url=None, realurl=None):
    if realurl:
        backend.getNewXls(realurl)
        backend.init()
        return
    if not url:
        return
    if backend.getNewXls(url):
        if tk_flag:
            showinfo('下载成功', 'XLS考试通知文件下载成功!')
        else:
            print('XLS考试通知文件下载成功!')
        backend.init()
    else:
        if tk_flag:
            showerror('下载失败', '未能成功下载XLS文件')
        else:
            print('未能成功下载XLS文件')


def clear_input(event):
    global cls_flag
    if cls_flag:
        ipt.delete(0, END)
        cls_flag = False
    elif event.char == '\r' or event.char == '\n':
        deal()


def main():
    global flag, ss
    if not backend.pre_check():
        with open(backend.base_dir + '.last_title', 'w') as f:
            f.write('\n\n')
            ss = ts % 'NONE'
        flag = True
    else:
        with open(backend.base_dir + '.last_title', 'r') as f:
            ss = ts % (f.read().split()[0])
    res = backend.new_note_check()
    if tk_flag:
        lb = Label(win, text=ss, justify='left')
        lb.pack()
        ipt.bind('<Key>', clear_input)
        ipt.pack()
        pre_text.set('搜索课程名称、教师名或班级(多个条件用空格分隔):')
        ipt.focus()

        bt = Button(win, text='查询', command=deal)
        bt.pack()
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
                        update(realurl=res)
                    else:
                        update(url=res)
                    lb.config(text=ts % res[1])
            else:
                update(realurl=res)
                showinfo('自动更新', '发现考试安排变更，已自动更新。')
        else:
            backend.init()
        win.mainloop()
    else:
        if res == -1:
            print('检测文件更新失败', '设备未联网' + ('且无可用考试安排文件，程序自动退出。' if flag else ''))
            if flag:
                exit('No Network')
        elif res:
            if res[-1]:
                if flag:
                    ask = True
                else:
                    ask = input('发现新的考试安排:\n    ' + res[1] + '\n\n是否更新考试安排文件?[y/n]:')
                if ask or ask in 'yY':
                    if flag:
                        update(realurl=res)
                    else:
                        update(url=res)
            else:
                update(realurl=res)
                print('发现考试安排变更，已自动更新。')
        else:
            backend.init()
        while True:
            target = input('输入查询信息: ')
            if target:
                print(backend.search(target))
            else:
                break


if __name__ == '__main__':
    main()

import cv2
import numpy as np
import os
from tkinter import ttk
import tkinter as tk
import tkinter.filedialog

def ls(dirs):
    global file_list
    try:
        for l in os.listdir(dirs):
            path = os.path.join(dirs,l)
            if os.path.isdir(path):ls(path)
            else:file_list.append(str(path))
    except:pass

def lsdir(dirs):
    global dir_list
    for l in os.listdir(dirs):
        path = os.path.join(dirs,l)
        if os.path.isdir(path):
            dir_list.append(path)
            lsdir(path)

def rm_dir(dir_name='./out_put'):
    global file_list,dir_list
    file_list = []
    ls(dir_name)
    for i in file_list:os.remove(i)
    dir_list = []
    lsdir(dir_name)
    for i in dir_list[::-1]:os.rmdir(i)

def get_frame(path,step = 15,file = 'png'):
    if path == '':
        tkinter.messagebox.showerror('错误','请先打开文件')
        return False
    if step <= 0:tkinter.messagebox.showerror('错误','错误的步长')
    try:os.mkdir('./out_put/'+os.path.basename(path).split('.')[0])
    except:
        if not tkinter.messagebox.askyesno('提示', '目录已存在,是否替换当前内容?'):return True
        rm_dir()
        try:os.mkdir('./out_put/'+os.path.basename(path).split('.')[0])
        except:pass
    cap = cv2.VideoCapture(path)
    num = 0
    while True:
        ret, frame = cap.read()
        if not ret:break
        if num % step == 0:cv2.imwrite('./out_put/'+os.path.basename(path).split('.')[0]+'/%04d.'% (num//step)+file,frame)
        num+=1
    cap.release()

left_up = []
w = 0
h = 0

def cut_video(path):
    if path == '':
        tkinter.messagebox.showerror('错误','请先打开文件')
        return False
    global left_up,w,h
    if left_up == [] or w == 0 or h == 0:
        tkinter.messagebox.showerror('错误','请先确定裁切范围')
        return False
    cap = cv2.VideoCapture(path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('./out_put/'+os.path.basename(path).split('.')[0]+'.avi',fourcc, cap.get(cv2.CAP_PROP_FPS), (w,h))
    while True:
        ret, frame = cap.read()
        if not ret:break
        out.write(frame[left_up[1]:left_up[1]+h,left_up[0]:left_up[0]+w])
    cap.release()
    out.release()

start_place = []
end_place = []
def get_mouse(event, x, y, flags, param):
    global start_place,end_place
    if event == cv2.EVENT_LBUTTONDOWN or flags == 1:start_place = [x,y]
    elif event == cv2.EVENT_RBUTTONDOWN or flags == 2:end_place = [x,y]

def get_box(path):
    if path == '':
        tkinter.messagebox.showerror('错误','请先打开文件')
        return False
    tkinter.messagebox.showinfo('提示','左键确定方框角上一点\n右键确定对角上另一点')
    global start_place,end_place,left_up,w,h
    cap = cv2.VideoCapture(path)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        tkinter.messagebox.showerror('错误','无法打开文件')
        return False
    cv2.namedWindow('show', cv2.WINDOW_KEEPRATIO)
    cv2.setMouseCallback('show', get_mouse)
    font = cv2.FONT_HERSHEY_SIMPLEX
    while True:
        img = frame.copy()
        if start_place != []:cv2.circle(img,start_place, 3, (0,255,0), -1)
        if end_place != []:cv2.circle(img,end_place, 3, (0,0,255), -1)
        if start_place != [] and end_place != []:
            cv2.rectangle(img,start_place,end_place,(255,0,0),2)
            left_up = [min(start_place[0],end_place[0]),min(start_place[1],end_place[1])]
            w = abs(start_place[0] - end_place[0])
            h = abs(start_place[1] - end_place[1])
            cv2.putText(img,'(%3d,%3d) width:%3d heitht:%3d' % (left_up[0],left_up[1],w,h),(10,40), font, 1,(255,255,255),5)
            cv2.putText(img,'(%3d,%3d) width:%3d heitht:%3d' % (left_up[0],left_up[1],w,h),(10,40), font, 1,(0,0,0),2)
        else:
            cv2.putText(img,'Press ESC to exit',(10,40), font, 1,(255,255,255),5)
            cv2.putText(img,'Press ESC to exit',(10,40), font, 1,(0,0,0),2)
        cv2.imshow('show',img)
        if cv2.waitKey(1) == 27:break
    pos.set('(%3d,%3d) width:%3d heitht:%3d' % (left_up[0],left_up[1],w,h))
    cv2.destroyAllWindows()

def get_fn():
    entry.delete(0,tk.END)
    entry.insert(0,tkinter.filedialog.askopenfilename())

try:os.mkdir('./out_put')
except:pass

root = tk.Tk() 
root.title("视频工具箱")
root.geometry("960x560+10+10")
root["bg"] = "#39C5BB"
tk.Label(root, text="视频工具箱",bg="#39C5BB",font=('Simhei',25)).place(x = 350, y = 5)
entry = tk.Entry(root, width=40 ,bd = 2,font=('Simhei',30))
entry.place(x = 0, y = 50)
tk.Button(root, text = "打开", command = get_fn, width=15 ,height=2,activeforeground='#39C5BB',font=('Simhei',14)).place(x = 805, y = 48)
pos = tk.StringVar()
pos.set('(XXX,XXX) width:XXX heitht:XXX')
tk.Label(root, textvariable=pos,bg="#39C5BB",font=('Simhei',24)).place(x = 10, y = 105)
tk.Button(root, text = "选择区域", command = lambda: get_box(entry.get()), width=12 ,height=2,activeforeground='#39C5BB',font=('Simhei',14)).place(x = 510, y = 100)
tk.Button(root, text = "输出", command = lambda: cut_video(entry.get()), width=8 ,height=2,activeforeground='#39C5BB',font=('Simhei',14)).place(x = 650, y = 100)
tk.Button(root, text = "打开文件资源管理器", command = lambda: os.system('start .\\out_put'), width=20 ,height=2,activeforeground='#39C5BB',font=('Simhei',14)).place(x = 750, y = 100)
tk.Label(root, text="切片步长:",bg="#39C5BB",font=('Simhei',25)).place(x = 10, y = 152)
step_len = tk.IntVar()
step_len.set(15)
tk.Entry(root,textvariable=step_len, width=5 ,bd = 2,font=('Simhei',30)).place(x = 170, y = 150)
able_type = ['png','jpg','bmp','tif','bpm']
p_type = tk.IntVar()
p_type.set(0)
tk.Radiobutton(root, text="PNG", variable=p_type,bg="#39C5BB",font=('Simhei',25), value=0).place(x = 450, y = 152)
tk.Radiobutton(root, text="JPG", variable=p_type,bg="#39C5BB",font=('Simhei',25), value=1).place(x = 550, y = 152)
tk.Radiobutton(root, text="BMP", variable=p_type,bg="#39C5BB",font=('Simhei',25), value=2).place(x = 650, y = 152)
tk.Radiobutton(root, text="TIF", variable=p_type,bg="#39C5BB",font=('Simhei',25), value=3).place(x = 750, y = 152)
tk.Radiobutton(root, text="BPM", variable=p_type,bg="#39C5BB",font=('Simhei',25), value=4).place(x = 850, y = 152)
tk.Button(root, text = "开始切片", command = lambda: get_frame(entry.get(),step = step_len.get(),file=able_type[p_type.get()]), width=15 ,height=2,activeforeground='#39C5BB',font=('Simhei',14)).place(x = 280, y = 148)
root.mainloop()

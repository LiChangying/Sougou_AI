#-*-encoding:utf-8-*-

import os
import sys
import tkinter as tk
from  tkinter import filedialog
from tkinter import ttk
import time
# # 创建全局变量
# file_num = 0
# file_cnt = 0
import json

src_file_path = ''
'''
    选择单个文件
'''
def select_src_file():
    # 选择文件path_接收文件地址
    src_file_path = tk.filedialog.askopenfilename().replace('/','\\')
    if src_file_path != '':
        print(src_file_path)
        entry_src_file_path_input.delete(0, tk.END)  # 清空文本框
        entry_src_file_path_input.insert(tk.END, src_file_path)  # 填充文本框
'''
    选择文件夹
'''
def select_src_folder():
    global src_file_path
    src_file_path = tk.filedialog.askdirectory().replace('/','\\')
    if src_file_path != '':
        print(src_file_path)
        entry_src_file_path_input.delete(0,tk.END)          #清空文本框
        entry_src_file_path_input.insert(tk.END,src_file_path)  #填充文本框



def test():
    inputdir = src_file_path
    for roots, folders, files in os.walk(inputdir):
        for file in files:
            if file.endswith('json'):
                with open(os.path.join(roots, file), 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    cnt = 0
                    for key, value in content.items():
                        cnt += 1
                        for item in value['regions']:
                            text = item['region_attributes']['text']
                            try:
                                qtype, qtext, qjudge = text.split('_')
                            except:
                                print(key, text, '转写格式异常，请检查')
                                continue
                            if qtype not in ['a', 'b', 'c', 'd', 'o']:
                                print(key, text, qtype, '题目类型异常(a b c d o)', end='\t')
                            if qtext.strip() == '' or 'x' in qtext or '（' in qtext or '）' in qtext:
                                print(key, text, qtext, '题目转写异常(为空,含有中文字符)', end='\t')
                            if qjudge not in ['wrong', 'right']:
                                print(key, text, qjudge, '批改异常(wrong right)')
                spam = list(set(content.keys()))
                if cnt != len(spam):
                    print('存在重复文件，重复文件为：')
                    for item in content.keys():
                        if item in spam:
                            spam.remove(item)
                        else:
                            print(item)
'''
    创建窗口
'''
def create_window(title,win_width,win_height):
    # 第1步，实例化object，建立窗口window
    window = tk.Tk()
    # 第2步，给窗口的可视化起名字
    window.title(title)
    # 第3步，设定窗口的大小(长 * 宽)
    window.geometry("%sx%s" %(win_width,win_height))  # 这里的乘是小x
    return window

'''
    创建frame
'''
def set_frame(window):
    frame = tk.Frame(window)
    #放置
    frame.pack()
    return frame


if __name__ == "__main__":
    src_format = ''
    tgt_format = ''
    window = create_window('Audio trans', 500, 500)
    # 创建一个top frame
    top_frame = set_frame(window)
    # 创建四个子frame
    audio_trans_frame = set_frame(top_frame)
    tk.Label(audio_trans_frame,width=70,height=2,text="========================Audio trans========================").pack()
    first_frame = set_frame(top_frame)
    second_frame = set_frame(top_frame)
    thrid_frame = set_frame(top_frame)
    fourth_frame = set_frame(top_frame)

    # 给第一个frame添加元素,按照表格布局，1x4
    ## 创建标签，源文件路径
    label_src_file_path = tk.Label(first_frame, width=10, height=2, text="源文件路径")
    label_src_file_path.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0)

    ## 创建单行输入框
    src_file_path = ''
    src_file_path = tk.StringVar(first_frame, value=src_file_path)
    entry_src_file_path_input = tk.Entry(first_frame, width=25, textvariable=src_file_path)
    entry_src_file_path_input.grid(row=0, column=1, padx=0, pady=0, ipadx=0, ipady=0)

    ## 创建文件类型选择框text=text, variable=file_type_var, value=value, command=command)
    radiobutton_path_type_file = tk.Radiobutton(first_frame, text="文件", value="file", command=select_src_file)
    radiobutton_path_type_file.grid(row=0, column=2, padx=0, pady=0, ipadx=0, ipady=0)
    radiobutton_path_type_folder = tk.Radiobutton(first_frame, text="文件夹", value="folder", command=select_src_folder)
    radiobutton_path_type_folder.grid(row=0, column=3, padx=0, pady=0, ipadx=0, ipady=0)


    # 给fourth_format添加控件
    ## 创建开始button
    button_begin = tk.Button(fourth_frame, text="Begin", command=test)
    button_begin.grid(row=0, column=1, padx=20, pady=0, ipadx=0, ipady=0)





    # 主窗口循环显示
    window.mainloop()


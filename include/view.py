#!/usr/bin/python3.5
import os
import sys
import re
import xml.sax
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
from tkinter.ttk import *
from . import dialog
from .dialog import Dialog
from tkinter.filedialog import askdirectory
from functools import partial

# TODO: display the repo and its path
# For example: Clemson - /users/Guoze/20_test --Paper Tracker V1.0
TITLE = "Paper Tracker V1.0"
GEOMETRY = '1060x580+200+50'
WIDTH=50
HEIGHT=10
SMALLFONT = ('Arial', 8)
MIDFONT  = ('Arial', 10)
LARGEFONT = ('Arial', 12)

class Controller(object):
  def __init__(self):
    pass

class RespInfoDialog(Dialog):
  def body(self, master):
    Label(master, text='New repository Name: ').grid(row=0,sticky=E)
    Label(master, text='Path of this repository: ').grid(row=1,sticky=E)
    Label(master, text='Support Suffix: ').grid(row=2,sticky=E)
    def selectPath():
      path_ = askdirectory()
      path.set(path_)
    path = StringVar()
    Button(master, text = "Browse...", command = selectPath).grid(row=1, column = 2)

    self.e1 = Entry(master)
    self.e2 = Entry(master,textvariable = path)
    self.e3 = Entry(master)
    self.e1.insert(0, "Example")
    # self.e2.insert(0, "d:\\01_test\\")
    self.e2.insert(0, "/home/guoze/02_test/")
    self.e3.insert(0, "pdf mobi")

    self.e1.grid(row=0, column=1)
    self.e2.grid(row=1, column=1)
    self.e3.grid(row=2, column=1)
    return self.e1 # initial focus

  def validate(self):
    try:
      rep_name = str(self.e1.get().strip())
      rep_path = str(self.e2.get().strip())
      support_suffix = str(self.e3.get().strip())
      support_suffix = support_suffix.split()
      self.result = [rep_name, rep_path, support_suffix]
      self.res_nums = len(self.result)
      return 1
    except (FileNotFoundError,ValueError):
      tkinter.messagebox.showwarning(
        "Bad input",
        "Illegal values, please try again"
      )
      return 0

class SelectRepDialog(Dialog):
  def body(self, master):
    self.rep_list = tk.Listbox(master)
    self.rep_list.config(fg='black', bg='#F5F5F5', bd=0.2, font=MIDFONT )
    self.rep_list.config(width=WIDTH, height=HEIGHT)

    scrollbar = tk.Scrollbar(master,orient=VERTICAL,command=self.rep_list.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    self.rep_list.configure(yscrollcommand=scrollbar.set)

    self.rep_list.grid(row=0)
    self.rep_list.bind("<Double-Button-1>", self.ok)
    self.rep_list.bind("<<ListboxSelect>>", self.selected)
    self.update_list()

  def selected(self, event):
    widget = event.widget
    selection=widget.curselection()
    value = widget.get(selection[0])
    self.selected_value = value

  def update_list(self):
    rep_dict = self.argv.get("all_repositories", {})
    if len(list(rep_dict.keys())) != 0:
      for i, one_rep in enumerate(rep_dict):
        rep_name = one_rep
        rep_path = rep_dict[one_rep][0]
        rep_suffix = ' '.join(str(e) for e in rep_dict[one_rep][1])
        rep_information = str(rep_name)+" ("+str(rep_path)+") "+ str(rep_suffix)
        self.rep_list.insert(tk.END, rep_information)

  def apply(self):
    rep_info = self.selected_value.split()
    rep_name = rep_info[0]
    self.result = rep_name
    self.res_nums= len(self.result)


class EditPaperDialog(Dialog):
  def body(self, master):
    if self.argv2 == 1:
      self.paper_info = self.argv
      self.paper_id = int(self.paper_info[0])
      paper_name = "Paper: "+ str(self.paper_info[1])
      old_importance = int(self.paper_info[2])
      old_urgency = int(self.paper_info[3])
      old_tags = str(self.paper_info[4])
      old_read = str(self.paper_info[5])
    else:
      paper_name = self.argv
    Label(master, text=paper_name,font=MIDFONT).grid(row=0,columnspan=2, sticky=W)
    Label(master, text='Importance(1~5): ').grid(row=1,sticky=E)
    Label(master, text='Urgency(1~5): ').grid(row=2,sticky=E)
    Label(master, text='Tags: ').grid(row=3,sticky=E)
    Label(master, text='Read(y/n): ').grid(row=4,sticky=E)
    self.paper_info = self.argv
    self.e1 = Entry(master)
    self.e2 = Entry(master)
    self.e3 = Entry(master)
    self.e4 = Entry(master)
    if self.argv2 == 1:
      self.e1.insert(0, old_importance)
      self.e2.insert(0, old_urgency)
      self.e3.insert(0, old_tags)
      self.e4.insert(0, old_read)

    self.e1.grid(row=1, column=1)
    self.e2.grid(row=2, column=1)
    self.e3.grid(row=3, column=1)
    self.e4.grid(row=4, column=1)
    return self.e1 # initial focus

  def validate(self):
    try:
      importance = int(self.e1.get().strip())
      urgency = int(self.e2.get().strip())
      tags = str(self.e3.get().strip())
      read_state = str(self.e4.get().strip())
      if importance < 1 or importance >5:
        raise ValueError("OutOfRange")
      if urgency < 1 or urgency >5:
        raise ValueError("OutOfRange")
      if self.argv2 == 1:
        self.result = [self.paper_id, importance, urgency, tags, read_state]
      else:
        self.result = [importance, urgency, tags, read_state]
      self.res_nums = len(self.result)
      return 1
    except ValueError:
      tkinter.messagebox.showwarning(
        "Bad input",
        "Illegal values, please try again"
      )
      return 0

  def apply(self):
    pass


class View(object):
  def __init__(self, controller):
    self.root = tk.Tk()
    # self.root.iconbitmap(default=".\\task_tracker.ico")
    self.root.title(TITLE)
    self.controller = controller
    self.root.bind('<Escape>', lambda event: self.controller.quit())
    self.search_mode = tk.StringVar()
    self.search_mode.set(4)
    self.rep_name = ""
    self.rep_path = ""
    self.paper_nums = 0
    self.paper_info = []
    self.path = StringVar()
    self.search_mode = tk.StringVar()
    self.search_mode.set(1)
    self.init()


  def init(self):
    # ***** Main Menu *****
    menubar = tk.Menu(self.root,  bg="lightgrey", fg="black",font=MIDFONT)
    # Create the Menu button in the Menu
    filemenu = tk.Menu(menubar,tearoff=0)
    filemenu.add_command(label="New Repository", command=self.new_rep)
    filemenu.add_command(label="Open Repository...",command = self.open_rep)
    filemenu.add_command(label="Delete Repository...",command = self.delete_rep)
    # filemenu.add_command(label="Close Repository",command=self.notYet)
    # filemenu.add_command(label="Open Recent",command=self.notYet)
    filemenu.add_command(label="Update data", command=self.update_data )
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=lambda event: self.controller.quit())
    menubar.add_cascade(label="File", menu=filemenu)
    # Create the Edit button in the Menu
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Edit Info", command=self.editPaper)
    # editmenu.add_command(label="Open Paper", command=self.open_paper)
    editmenu.add_command(label="Show Tags",command=self.show_tags)
    editmenu.add_command(label="Show Paper Path",command=self.show_paper_path)
    editmenu.add_command(label="Get Rec Papers",command=self.get_recommend_papers)
    menubar.add_cascade(label="Edit", menu=editmenu)
    # Create the help button in the Menu
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Introduce...",command=self.show_introduce)
    helpmenu.add_separator()
    helpmenu.add_command(label="About", command = self.show_about)
    menubar.add_cascade(label="Help", menu=helpmenu)
    self.root.config(menu=menubar)

    # ***** Function part *****
    # Create the search entry and search buttom
    self.func_frame = tk.Frame(self.root, width=300, height=30)
    self.search_frame = tk.Frame(self.func_frame, width=300)
    self.search1_frame = tk.Frame(self.search_frame, width=180)
    self.search2_frame = tk.Frame(self.search_frame, width=180)
    self.button_frame= tk.Frame(self.func_frame, width=120)

    self.search1_frame.pack(side="top", fill="both",expand=True)
    self.search2_frame.pack(side="top", fill="both",expand=True)

    self.entryBox = tk.Entry(self.search1_frame, width=60, font=LARGEFONT)
    self.entryBox.bind('<Return>', (lambda event: self.search()))
    self.entryBox.pack(padx=10, pady=10,anchor="s")

    # Create the serch mode Button
    label_text = tk.Label(self.search2_frame, text="Search Mode: ")
    label_text.pack(padx=10,side="left",anchor="n")
    radioButton_1 = tk.Radiobutton(self.search2_frame, text ="Name",
                                   variable = self.search_mode, value = 1)
    radioButton_1.pack(side="left",anchor="n")
    radioButton_2 = tk.Radiobutton(self.search2_frame, text ="Tags",
                                   variable = self.search_mode, value = 2)
    radioButton_2.pack(side="left",anchor="n")
    # radioButton_3 = tk.Radiobutton(self.search2_frame, text ="Nums",
    #                                variable = self.search_mode, value = 3)
    # radioButton_3.pack(side="left",anchor="n")
    radioButton_4 = tk.Radiobutton(self.search2_frame, text ="ID",
                                   variable = self.search_mode, value = 4)
    radioButton_4.pack(side="left",anchor="n")
    search_button = tk.Button(self.button_frame, text="Search", width=20,
                              command=self.search)
    search_button.pack(padx=10,pady=10,anchor="s")

    self.search_frame.pack(side=LEFT, fill="both")
    self.button_frame.pack(side=RIGHT, fill ="both")

    # ***** Display Label *****
    self.display_frame = tk.Frame(self.root, width=300, height=30)
    self.display_frame.pack_propagate(0)
    # rep_info_frame = tk.Frame(self.display_frame,width=300)
    # rep_info_frame.pack(side="top",fill="both",expand=True)


    # label_text = tk.Label(rep_info_frame,text="Repo_name: ")
    # label_text.pack(side="left",fill="x",anchor="e")
    # label_repo_name = tk.Label(rep_info_frame,text="/user/Guoze", anchor="w")
    # label_repo_name.pack(side="right",fill="x",anchor="w")
    # label_folder_label.pack(side=TOP)

    # label_text = tk.Label(root,text="Quantity of Paper: ",anchor="e",width=20)
    # label_text.pack(side=TOP)
    # label_num_label = tk.Label(root,text="50",anchor="w",width=20)
    # label_num_label.pack(side=TOP)

    # label_text = tk.Label(root,text="Code Base Folder: ",anchor="e",width=20)
    # label_text.pack(side=TOP)
    # label_folder_label = tk.Label(root,text="/user/Guoze", anchor="w",width=20)
    # label_folder_label.pack(side=TOP)

    # # label_text = tk.Label(root,text="Code TODO: ",anchor="e",width=20)
    # # label_text.grid(row=3, column = display_column, sticky=E)
    # # label_folder_label = tk.Label(root,text="50",anchor="w",width=20)
    # # label_folder_label.grid(row = 3, column = display_column+1,sticky=W)

    # # ***** Table For Paper Information *****
    tree_columns=("a", "b", "c", "d", "e","g","h")
    self.table_frame = tk.Frame(self.root, width=600)
    self.tree = ttk.Treeview(self.table_frame,show="headings", height=20,
                              columns=tree_columns)
    self.vbar = tk.Scrollbar(self.table_frame, orient=VERTICAL, command=self.tree.yview)
    self.tree.configure(yscrollcommand=self.vbar.set)
    self.vbar.config( command = self.tree.yview )
    self.tree.configure(yscrollcommand=self.vbar.set)
    self.tree.column("a", width=50, anchor="center")
    self.tree.column("b", width=300, anchor="center")
    self.tree.column("c", width=50, anchor="center")
    self.tree.column("d", width=50, anchor="center")
    self.tree.column("e", width=100, anchor="center")
    self.tree.column("g", width=50, anchor="center")
    self.tree.column("h", width=50, anchor="center")
    self.tree.heading("a", text="ID")
    self.tree.heading("b", text="Name")
    self.tree.heading("c", text="Importance")
    self.tree.heading("d", text="Urgency")
    self.tree.heading("e", text="Tags")
    self.tree.heading("g", text="Read")
    self.tree.heading("h", text="Date")
    # self.update_table()
    self.tree.pack(side="left", fill="both", expand=True)
    self.tree.bind('<ButtonRelease-1>', self.treeviewClick)
    self.tree.bind('<Double-Button-1>', self.treeviewDubClick)
    self.vbar.pack(side="right",fill="y")
    for col in tree_columns:
      self.tree.heading(col, command=lambda _col=col: self.treeview_sort_column(self.tree, _col, False))

    # # ***** Status Bar *****
    self.status_frame = tk.Frame(self.root)
    self.status = tk.Label(self.status_frame, text=str(self.rep_name))
    self.status.pack(side="left")
    # label_text = tk.Label(self.search2_frame, text="Search Mode: ")
    # label_text.pack(padx=10,side="left",anchor="n")

    self.func_frame.grid(row=0,column=0,rowspan=2,columnspan=2,sticky= "ew")
    self.display_frame.grid(row=0, column=2, rowspan=2,sticky= "ew")
    self.table_frame.grid(row=2,column=0,columnspan=3,sticky= "nsew")
    self.status_frame.grid(row=3,column=0,columnspan=3,sticky="ew")

    self.root.grid_rowconfigure(1, weight=1)
    self.root.grid_columnconfigure(1, weight=1)

  def editPaper(self):
    if len(self.paper_info) == 0:
      self.show_err("Please Choose one paper firstly.")
    else:
      self.controller.change_paper_info(self.paper_info)

  def treeviewClick(self,event):
    for item in self.tree.selection():
        item_text = self.tree.item(item,"values")
        self.paper_info = item_text

  def treeviewDubClick(self,event):
    for item in self.tree.selection():
        item_text = self.tree.item(item,"values")
        self.controller.change_paper_info(item_text)

  def treeview_sort_column(self, tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

  # ***** Implement For the Menu button *****
  def search(self):
    search_mode = int(self.search_mode.get())
    search_string = self.entryBox.get()
    if search_string:
      def search_by_name(name):
        return self.controller.query_by_name(name)

      def search_by_tags(tags_s):
        return self.controller.query_by_tags(tags_s)

      def search_by_nums(num_s):
        return self.controller.query_by_nums(num_s)

      def search_by_id(id_num):
        return self.controller.query_by_id(id_num)

      if search_mode == 4:
        res_papers = search_by_id(search_string)
      elif search_mode == 2:
        res_papers = search_by_tags(search_string)
      elif search_mode == 3:
        res_papers = search_by_nums(search_string)
      else:
        res_papers = search_by_name(search_string)

      if res_papers:
        self.update_papers_table(res_papers)
      else:
        self.show_err("Can't find any papers.")
    else:
      self.update_data()

  def open_paper(self):
    paper_num = None
    if len(self.paper_info) == 0:
      self.show_err("Please Choose one paper firstly.")
      return False
    else:
      paper_num = self.paper_info[0]
      open_res = self.controller.open_paper_by_num(paper_num)

  def get_recommend_papers(self):
    rec_papers = self.controller.get_recommend_papers()
    if rec_papers:
      self.update_papers_table(rec_papers)
    else:
      self.show_err("No Paper in this repo.")

  # ***** Ask Controller *****
  def new_rep(self):
    rep_info = self.new_rep_dialog()
    if rep_info is False:
      return False
    else:
      res = self.controller.add_repository(rep_info)
      if res == False:
        self.show_err()
      else:
        rep_name = rep_info[0]
        res = self.controller.select_rep(rep_name)
        if res:
          self.rep_name = res[0]
          rep_info = "Rep: "+ str(self.rep_name)
          self.rep_path = res[1]
          rep_info = rep_info + " ("+ str(self.rep_path) +")"
          self.status.config(text=rep_info)

  def open_rep(self):
    rep_dict = self.controller.get_all_repository()
    if len(list(rep_dict.keys())) != 0:
      rep_name = self.reps_dialog(rep_dict,1)
      res = self.controller.select_rep(rep_name)
      if res:
        self.rep_name = res[0]
        rep_info = "Rep: "+ str(self.rep_name)
        self.rep_path = res[1]
        rep_info = rep_info + " ("+ str(self.rep_path) +")"
        self.status.config(text=rep_info)
    else:
      self.show_err()

  def delete_rep(self):
    rep_dict = self.controller.get_all_repository()
    if len(list(rep_dict.keys())) != 0:
      rep_name = self.reps_dialog(rep_dict,0)
      res = self.controller.delete_rep(rep_name)
      if res == 0:
        self.show_err("Please close this Repository before your delete it.")

  def update_data(self):
    self.controller.refresh_papers()
    self.controller.update_papers_table()

  # ***** For Controller to call *****
  def ask_paper_info(self,paper_name):
    resDialog = EditPaperDialog(self.root,'Edit Paper Infomation', paper_name,0)
    if resDialog.result is None:
      return False
    else:
      return resDialog.result

  def reps_dialog(self,reps,op):
    if op == 1:
      resDialog = SelectRepDialog(self.root,'Open Repository',reps)
    if op == 0:
      resDialog = SelectRepDialog(self.root,'Delete Repository',reps)
    if resDialog.res_nums == 0:
      return False
    else:
      return resDialog.result

  def new_rep_dialog(self):
    resDialog = RespInfoDialog(self.root,'Create a New Repository')
    if resDialog.res_nums == 0:
      return False
    else:
      return resDialog.result

  def edit_paper_info(self, paper_info=None):
    resDialog = EditPaperDialog(self.root,'Edit Paper Infomation', paper_info, 1)
    if resDialog.result is None:
      return False
    else:
      return resDialog.result

  def update_papers_table(self, recs):
    def prettify_one(rec):
      one_row = [str(rec[7]),
                rec[0],
                str(rec[1]),
                str(rec[2]),
                rec[3],
                str(rec[5]),
                rec[6]]
      one_row = [item for item in one_row]
      return one_row
    recs_t = [prettify_one(rec) for rec in recs]
    for _ in map(self.tree.delete, self.tree.get_children("")):
      pass
    self.paper_nums = len(recs_t)
    for i in range(len(recs_t)):
      self.tree.insert("", "end", values=(recs_t[i][0],
                                          recs_t[i][1],
                                          recs_t[i][2],
                                          recs_t[i][3],
                                          recs_t[i][4],
                                          recs_t[i][5],
                                          recs_t[i][6]))
      # TODO: Find a function to update the data by the application
      # self.tree.after(10000, self.update_data)

  # ***** Show some Information *****
  def show_tags(self):
    tags = self.controller.get_all_tags()
    tags = "Tags: "+ str(tags)
    tkinter.messagebox.showinfo(
      "All Tags in this repo.",
      tags
    )

  def show_paper_path(self):
    paper_num = None
    if len(self.paper_info) == 0:
      self.show_err("Please Choose one paper firstly.")
      return False
    else:
      paper_num = self.paper_info[0]
      path = self.controller.get_paper_path_by_nums(paper_num)
      path = "Paper Path: "+ str(path)
      tkinter.messagebox.showinfo(
        "Path:",
        path
      )

  def show_introduce(self):
    tkinter.messagebox.showinfo(
      "Introduce",
      "Please followed the Intoduce.pdf in the source code directory!"
    )

  def show_about(self):
    tkinter.messagebox.showinfo(
      "About",
      "Paper Tracker: Version: V1.0"
    )

  # TODO: Finish this function
  def show_err(self,err_info=None):
    if err_info is None:
      tkinter.messagebox.showinfo(
        "Error",
        "Paper Tracker: Version: V1.0"
      )
    else:
      tkinter.messagebox.showinfo(
        "Error",
        err_info
      )

  def notYet(self):
    tkinter.messagebox.showinfo('Oops', 'Not implemented Yet!')


if __name__ == "__main__":
  view = View(Controller())
  tk.mainloop()

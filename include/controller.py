#!/usr/bin/python3.5
import os
import sys
import tkinter as tk
from . import view
from . import model
from .model import *
from . import repository
from .repository import *

class Controller(object):

  def __init__(self):
    self.paper_manager = model.Manager_Paper()
    self.view = view.View(self)
    self.view.open_rep()
    # self.paper_manager.refresh()

  # *****Repository API *****
  def get_all_repository(self):
    rep_dict = self.paper_manager.get_all_repository()
    return rep_dict

  def add_repository(self, rep_info):
    self.paper_manager.add_repository(rep_info)
    self.refresh_papers()
    self.update_papers_table()

  def select_rep(self, rep_name):
    res = self.paper_manager.select_repository(rep_name)
    if res:
      self.refresh_papers
      self.update_papers_table()
      return res
    else:
      return False

  def delete_rep(self, rep_name):
    res = self.paper_manager.delete_repository(rep_name)
    if res:
      self.refresh_papers()
      return True
    else:
      return False

  def get_all_tags(self):
    paper_tags = self.paper_manager.get_all_tags()
    return paper_tags

  # ***** View API *****
  def update_papers_table(self):
    # self.refresh()
    self.refresh_papers()
    recs = self.paper_manager.get_all_papers()
    self.view.update_papers_table(recs)
    return True

  # ***** Paper information API  *****
  def get_recommend_papers(self):
    rec_papers = self.paper_manager.get_recommend_papers()
    return rec_papers

  def open_paper_by_num(self, num_s):
    res = self.paper_manager.open_paper_by_num(num_s)
    return res

  def change_paper_info(self,paper_info):
    paper_info = self.view.edit_paper_info(paper_info)
    if paper_info is not False:
      paper_id,paper_im, paper_ug, paper_tags, read = paper_info
      self.paper_manager.edit_one_paper(paper_id,paper_im, paper_ug, paper_tags, read)
      self.update_papers_table()

  def open_paper_by_num(self,num_s):
    self.paper_manager.open_paper_by_num(num_s)
    return True

  def del_paper_by_name(self, names):
    self.paper_manager.del_paper_by_name(names)
    return True

  def get_paper_path_by_nums(self, nums):
    res = self.paper_manager.get_paper_path_by_nums(nums)
    return res
  # ***** Search API *****
  # TODO(Guoze):Complete this function
  def query_by_name(self, name_s):
    res_papers = self.paper_manager.query_by_name(name_s)
    return res_papers

  def query_by_tags(self, tags_s):
    res_papers = self.paper_manager.query_by_tags(tags_s)
    return res_papers

  def query_by_nums(self, num_s):
    res_papers = self.paper_manager.query_by_nums(num_s)
    return res_papers 

  def query_by_id(self,id_num):
    res_papers = self.paper_manager.query_by_id(id_num)
    return res_papers

  # Refresh the papers in the repo and ask user to add papers infomation
  # Called: select repo || new_repo || delete repo || update table
  def refresh_papers(self):
    new_papers = self.paper_manager.refresh()
    def add_paper_info(new_paper):
      return self.view.ask_paper_info(new_paper) 
    for paper in new_papers:
      # TODO(Guoze): Create a Paper class to manager this
      paper_im, paper_ug, paper_tags, read = add_paper_info(paper)
      self.paper_manager.insert_one(paper, paper_im, paper_ug, paper_tags, read)

  # ***** System API *****
  def quit(self):
    self.paper_manager.quit_paper_manager()
    exit(0)

if __name__ == "__main__":
  controller = Controller()
  tk.mainloop()
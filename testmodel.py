import os
import sys
import unittest
import json
import sqlite3
import shutil
import include.model as model
from include.model import Manager_Paper

class TestManager_Paper(unittest.TestCase):
  def setUp(self):
    self.paper_manager = model.Manager_Paper()
    self.base_path = os.path.abspath(os.curdir)
    self.paper_manager.db_path = os.path.join(self.base_path,
                                                "test_paper_manager.db")
    self.paper_manager.user_config_path = os.path.join(self.base_path,
                                                        "test_user_config.json")
    self.paper_manager.conn = sqlite3.connect(self.paper_manager.db_path)
    self.paper_manager.cursor = self.paper_manager.conn.cursor()
    self.paper_path = os.path.join(self.base_path, "test_paper")
    if not os.path.exists(self.paper_path):
      os.makedirs(self.paper_path)
    for i in range(5):
      paper = self.paper_path+"/"+ str(i) +".pdf"
      f = open(paper,'w')
      f.write("Test")
      f.close()
    self.test_reps=["Tang",self.paper_path,"pdf"]
    self.paper_manager.add_repository(self.test_reps)
    for i in range(3):
      paper_name = str(i) + ".pdf"
      self.paper_manager.insert_one(paper_name,i,i,"Network"+str(i),"n")

  def tearDown(self):
    self.paper_manager.conn.commit()
    self.paper_manager.cursor.close()
    self.paper_manager.conn.close()
    os.remove(self.paper_manager.db_path)
    os.remove(self.paper_manager.user_config_path)
    shutil.rmtree(self.paper_path)

  def test_get_user_config(self):
    if os.path.exists(self.paper_manager.user_config_path):
      with open(self.paper_manager.user_config_path) as f:
        expect_config = json.load(f)
    else:
      expect_config={}
    user_config = self.paper_manager.get_user_config()
    self.assertEqual(user_config, expect_config)

  def test_get_all_repository(self):
    self.assertEqual(self.paper_manager.get_all_repository(),
                    self.paper_manager.user_config)

  def test_add_repository(self):
    new_rep = ["New_rep",self.paper_path,"mobi"]
    self.paper_manager.add_repository(new_rep)
    self.paper_manager.select_repository("New_rep")
    self.assertEqual(self.paper_manager.cur_rep.path
                      ,self.paper_path)
    self.assertEqual(self.paper_manager.cur_rep.name
                      ,"New_rep")
    self.assertEqual(self.paper_manager.cur_rep.support_suffix
                      ,"mobi")


  def test_select_repository(self):
    self.paper_manager.select_repository("Tang")
    self.assertEqual(self.paper_manager.cur_rep.path
                      ,self.paper_path)
    self.assertEqual(self.paper_manager.cur_rep.name
                      ,"Tang")
    self.assertEqual(self.paper_manager.cur_rep.support_suffix
                      ,"pdf")

  def test_delete_repository(self):
    self.paper_manager.select_repository("Tang")
    self.assertFalse(self.paper_manager.delete_repository("Tang"))

    new_rep = ["New_rep",self.paper_path,"pdf"]
    self.paper_manager.add_repository(new_rep)
    self.assertTrue(self.paper_manager.delete_repository("Tang"))

  def test_refresh(self):
    new_papers = self.paper_manager.refresh()
    expect_papers=['3.pdf', '4.pdf']
    self.assertEqual(len(new_papers), len(expect_papers) )

  def test_get_all_papers(self):
    all_papers = self.paper_manager.get_all_papers()
    self.assertEqual(len(all_papers)
                      ,3)
    paper_name = "4.pdf"
    self.paper_manager.insert_one(paper_name,2,3,"Network","n")

    all_papers = self.paper_manager.get_all_papers()
    self.assertEqual(len(all_papers)
                      ,4)

  def test_edit_one_peper(self):
    paper_name = "4.pdf"
    self.paper_manager.insert_one(paper_name,2,3,"Test","n")

    all_papers = self.paper_manager.get_all_papers()
    index_paper = len(all_papers) - 1
    index_id = len(all_papers[3]) - 1
    index_tags = 3
    self.assertEqual(all_papers[index_paper][index_id]
                      ,4)
    self.assertEqual(all_papers[index_paper][index_tags]
                      ,"Test")
    paper_id = all_papers[index_paper][index_id]
    self.paper_manager.edit_one_paper(paper_id, 5, 5, "Update","y")

    all_papers = self.paper_manager.get_all_papers()
    self.assertEqual(all_papers[index_paper][index_tags]
                      ,"Update")

  def test_get_recommend_papers(self):
    rec_papers = self.paper_manager.get_recommend_papers()
    index_paper = 0
    index_name = 0
    self.assertEqual(rec_papers[index_paper][index_name]
                      ,"2.pdf")

  def test_get_all_tags(self):
    tags = self.paper_manager.get_all_tags()
    expect_tags = ['Network0', 'Network1', 'Network2']
    self.assertEqual(len(tags),len(expect_tags))

  def test_get_paper_path_by_nums(self):
    all_papers = self.paper_manager.get_all_papers()
    index_paper = len(all_papers) - 1
    index_id = len(all_papers[index_paper]) - 1
    index_name = all_papers[index_paper][0]
    paper_path = self.paper_manager.get_paper_path_by_nums(all_papers[index_paper][index_id])
    expect_path = self.paper_path+"/"+ str(index_name)
    self.assertEqual(paper_path,expect_path)

  def test_query_by_tags(self):
    search_tag = "Network2"
    res_paper = self.paper_manager.query_by_tags(search_tag)
    self.assertEqual(len(res_paper),1)

if __name__=="__main__":
  unittest.main()

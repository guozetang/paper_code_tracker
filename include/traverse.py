#!/usr/bin/python

import os, sys
import fnmatch
import stack

class Traverse(object):

  def __init__(self, dir):
    self.dir = dir
    self.files = []
    self.dirs = []

  def displayFiles(self):
    print "Files:"
    for x in t.files:
      print x
    print 'There are', len(t.files), "files:"

  def displayDirs(self):
    print 'The', len(t.dirs), "dirs:"
    for x in t.dirs:
      print x

  def walk(self):
    dirStack = stack.Stack()
    dirStack.push( self.dir )
    while not dirStack.empty():
      currDir = dirStack.top()
      dirStack.pop()
      files = os.listdir( currDir )
      for x in files:
        if fnmatch.fnmatch(x, '.*'):
          continue
        thisFile = os.path.join(currDir, x)
        if os.path.isdir(thisFile):
          self.dirs.append(thisFile)
          dirStack.push(thisFile)
        else:
          self.files.append(thisFile)

if __name__ == '__main__':
  dir = os.getcwd()
  t = Traverse(dir)
  t.walk()
  print 'There are', len(t.files), "files:"
  t.displayDirs()

# -*-coding:utf-8-*- 
import os
import codecs
# 全局变量
# 需要生成目录的文件夹
rootdir = './'
# 需要忽略的文件夹
ignorePathList = ['.git', '.obsidian', '.gitignore', 'README.md', 'markdown-symmary.py']


def listPath(rootDir, file):
  global rootdir
  global ignorePathList
#  print('rootDir' + rootDir)
  list = os.listdir(rootDir)
  for i in list:
    if i in ignorePathList:
      print('ignore dir')
      continue
    path = os.path.join(rootDir,i)
    if os.path.isdir(path):
      dirSize = len(os.path.relpath(path, rootdir).replace('\\', r'/').split("/"))
      print("dirSize: " + str(dirSize))
      print('-------start ' + path + '----------')
      #print('path' + str(os.path.relpath(path, rootdir).replace('\\', r'/').split("/")))
      print('rootDir' + str(rootDir))
      if dirSize == 1:
        #print('### %s\n' %(i))
        file.write('### %s\n' %(i))
      elif dirSize == 2:
        #print('#### %s\n' %(i))
        file.write('#### %s\n' %(i))
      elif dirSize == 3:
        #print('##### %s\n' %(i))
        file.write('##### %s\n' %(i))
      else:
        #print('###### %s\n' %(i))
        file.write('###### %s\n' %(i)) 
      listPath(path, file)
      print('-------end ' + path + '----------')
    else:
#      替换当前文件夹    
#       print('----' + os.path.relpath(path, rootdir) + '---' + i)
#       print('----' + os.path.normcase(os.path.relpath(path, rootdir)) + '---')

#       print(os.path.split(path))
#       print(os.path.splitext(i))

       #print('- [%s](./%s)：%s' %(os.path.splitext(i)[0], os.path.relpath(path, rootdir).replace('\\', r'/'), os.path.splitext(i)[0]))
       file.write('- [%s](./%s)：%s\n' %(os.path.splitext(i)[0], os.path.relpath(path, rootdir).replace('\\', r'/').replace(' ', ''), os.path.splitext(i)[0]))
       if ' ' in i:
           print("error name :{}".format(i))
       count = 0
       count += 1
#      print(path + 'is dir')
      
    


if __name__ == '__main__':
   # 生成的目录文件
   file = codecs.open(rootdir + '/CONTENTS.md', 'w', 'utf-8')
   file.write('')
   file.write('# 笔记目录\n')
   file.write('- [README](./README.md)：README\n')
   listPath(rootdir, file)
   file.close()

# -*-coding:utf-8-*- 
import os
import codecs
# 全局变量
# 需要生成目录的文件夹
rootdir = './'
# 需要忽略的文件夹
ignorePathList = ['.git', '.obsidian', '.gitignore', 'README.md', 'markdown-symmary.py', '.trash', 'LICENSE']


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

def tree(dir_path, md, prefix=0):
    contents = os.listdir(dir_path)
    
    # 将目录和文件分开并排序
    dirs = sorted([d for d in contents if os.path.isdir(os.path.join(dir_path, d))])
    files = sorted([f for f in contents if os.path.isfile(os.path.join(dir_path, f))])

    # 打印当前目录名
    # print(f"{prefix}+-- {os.path.basename(dir_path)}")
    prefix += 1

    # 先列出所有子目录
    for dir_name in dirs:
        if dir_name in ignorePathList:
            # print('ignore dir')
            continue
        dir_path_child = os.path.join(dir_path, dir_name)
        md.write(f"{'#' * (prefix + 1)} {dir_name}\n\n")
        tree(dir_path_child, md, prefix)

    # 最后列出所有文件
    # for file_name in files:
    for i, file_name in enumerate(files):
        if file_name in ignorePathList:
            # print('ignore dir')
            continue
        content_path = os.path.join(dir_path, file_name)
        relative_path = os.path.relpath(content_path, start=root_dir)
        # print(relative_path)
        md.write(f"{' ' * (prefix - 1)}- [{file_name}]({relative_path.replace(os.path.sep, '/')})\n")
        is_last = i == len(files) - 1
        if is_last:
            md.write('\n')


def generate_markdown_tree(root_dir, markdown_file):
    global rootdir
    rootdir = root_dir
    with open(markdown_file, 'w', encoding='utf-8') as md:
        # 写入标题
        md.write('# 笔记目录\n')
        md.write('- [README](./README.md)：README\n')
        # 调用递归函数
        tree(root_dir, md, 0)
# # 指定根目录
# output_markdown_file = 'markdown.md'
# root_dir = 'D:/workspace/learning/person-learning-note'
# generate_markdown_tree(root_dir, output_markdown_file)


if __name__ == '__main__':
   # 生成的目录文件
  #  file = codecs.open(rootdir + '/CONTENTS.md', 'w', 'utf-8')
  #  file.write('')
  #  file.write('# 笔记目录\n')
  #  file.write('- [README](./README.md)：README\n')
  #  listPath(rootdir, file)
  #  file.close()
  output_markdown_file = 'CONTENTS.md'
  root_dir = './'
  generate_markdown_tree(root_dir, output_markdown_file)
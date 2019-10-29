# 中国石油大学（北京）考试安排查询脚本  

[![](https://img.shields.io/badge/author-RhythmLian-blue)](https://img.shields.io/badge/author-RhythmLian-blue)
[![](https://img.shields.io/badge/version-2.4.2-green)](https://img.shields.io/badge/version-2.4.2-green)
[![](https://img.shields.io/badge/License-MIT-yellow)](https://img.shields.io/badge/License-MIT-yellow)

## 环境依赖:
```shell
pip3 install requests
pip3 install xlrd
```

## 下载
  - [点击下载](https://github.com/Rhythmicc/CUP_EXAM/archive/master.zip)

## 用法:
```shell
python3 frontend.py
```

- ### 为脚本添加命令

  ```shell
  python3 setup.py --clean
  ```

  如果添加命令成功，你可以运行下面的命令：

  ```
  exam
  ```

  来使用脚本。

- ### 可能的问题与解决方案
  |问题|解决方案|
  |:---|:---|
  |Windows添加命令仅局部有效问题|系统环境变量->PATH->编辑->末尾添加项目的文件夹地址|
  |程序意外解析xls文件失败(编码问题)|将项目下的`content.xls`删除并重新启动程序|
  |Windows没有`unzip`命令行工具|程序自动下载安装包并打开，需要手动[设置环境变量](#设置环境变量)|


## 运行结果:  

### New version 2.5

- 支持匹配更多的考试安排文件类型, 并输出合适的信息

### Old version 2.4.2

- 简化安装。

### Old version 2.4.1

- 更新：上线自动版本更新功能。

  ![10.png](./img/10.png)

- 问题:

  Windows系统可能没有“unzip"命令，程序将帮你下载安装程序，位置在运行程序的目录下。你需要手动安装它，并设置环境变量。

  #### 设置环境变量
  
  ```shell
  系统环境变量->PATH->编辑->尾部添加：“C:\Program Files (x86)\GnuWin32\bin;”
  ```

### Old version 2.3

- Update: add install.sh and start.sh to easy start.

  ![9.png](./img/9.png)

### Old version 2.2
- Update: Simplify search expressions and remove the dependency on the fuzzywuzzy library.   
  ![8.png](./img/8.png) 

### Old version 2.1
- Update: The program automatically maintains test scheduling files.  
  ![7.png](./img/7.png)  

### Old version 2.0  
- new feature  
  ![5.png](./img/5.png)  
  ![6.png](./img/6.png)  



- simple example  
  ![simple example](./img/4.png)  

### Old version 1.0  
![1.jpg](./img/1.jpg)  

- By the way, if the **content.xls** is existed, the program will not ask for a url. 

- And if you want to update it, you can delete it and input new url. 
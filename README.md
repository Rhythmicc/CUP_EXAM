# CUP_EXAM  

## Environment dependence:  
```shell
pip3 install requests
pip3 install xlrd
```

## Usage:  
```shell
python3 frontend.py
```

- ### Install

  ```shell
  python3 setup.py [--clean (which means remove additional shell)]
  ```

  And it will create a command 'exam'. 

  After that, you can run:

  ```
  exam
  ```

  to use program~

- ### Install issue 
  (Your Windows may not have command 'setx'. So you can only set PATH manually.)

  ```
  系统环境变量->PATH->新建->名称:exam, 值: (文件夹位置)\exam.bat
  ```


## Computational results:  

### New version 2.3

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
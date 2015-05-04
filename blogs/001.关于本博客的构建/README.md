#关于本博客的构建

##一、特性
基于Github的Readme文件构造，将博客做成一个由markdown文件构成的项目，用git、sublime等进行管理
####目录构造
``` 
    |-Blog
      |-blogs            // 所有文章存放目录
        |-001.Test Art1  // 文章目录，包含md文件和其引用的图片
           -README.md    // 文章的主文件
           -1.jpg
        |-002.Test Art2
      |-tags             // 标签索引存放目录
      |-template         // 自动化模版
      -auto.py           // 自动化索引工具
      -README.md         // index 主目录

```


##二、问题和解决
####问题
- 目录索引问题：首页需要有一个目录能够看到所有的博客标题，并且方便地跳转
- 标签归类问题：一般博客系统都有一个标签分类系统，用以对文章进行分类，所以这个必须有

####解决
用python实现了一个自动化构建工具[auto.py](https://github.com/yimun/Blog/blob/master/auto.py)，对于blogs文件夹下的文件进行提取标签，分类并创建标签列表(tags文件夹下的索引)，以及根目录索引的构建(README.md)

##三、博客工作流
####1.添加博客
```
python auto.py add articlename
```
![Screenshot](https://raw.githubusercontent.com/yimun/Blog/master/blogs/001.关于本博客的构建/1.png)

该命令默认在blogs目录下新建一个名为`序号+articlename`的目录，目录下默认文件为`README.md`,其中的默认模板是[new.md](https://github.com/yimun/Blog/blob/master/template/new.md)，文章在这里编辑

![Screenshot](https://raw.githubusercontent.com/yimun/Blog/master/blogs/001.关于本博客的构建/2.png)

####2.更新索引
```
python auto.py update
```
![Screenshot](https://raw.githubusercontent.com/yimun/Blog/master/blogs/001.关于本博客的构建/3.png)

tags目录更新后：

![Screenshot](https://raw.githubusercontent.com/yimun/Blog/master/blogs/001.关于本博客的构建/4.png)

根目录下的README.md更新后：

![Screenshot](https://raw.githubusercontent.com/yimun/Blog/master/blogs/001.关于本博客的构建/5.png)

####3.git提交
```
此处省略两三条命令...
```


---
*2015-05-04 17:31*
#关于本博客的构建

##一、特性
基于Github的Readme文件构造，将博客做成一个由markdown文件构成的项目，用git、sublime等进行管理
####文件构造
``` 
    |-Blog
      |-blogs           // 所有文章存放目录
        |-001....       // 文章目录，包含md文件和其引用的图片
           -README.md   // 文章的主文件
           -1.jpg
        |-002....
      |-tags            // 标签索引存放目录
      |-template
      -autoindex.py     // 自动化索引工具
      -README.md        // index 主目录

```

##二、问题和解决
####问题
- 目录索引问题：首页需要有一个目录能够看到所有的博客标题，并且方便地跳转
- 标签归类问题：一般博客系统都有一个标签分类系统，用以对文章进行分类，所以这个必须有

####解决
用python实现了一个自动化构建工具[autoindex.py](https://github.com/yimun/Blog/blob/master/autoindex.py)，对于blogs文件夹下的文件进行提取标签，分类并创建标签列表(tags文件夹下的索引)，以及根目录索引的构建(README.md)
```python
python autoindex.py update          // 更新目录
python autoindex.py add articlename // 添加文章(待实现)

```
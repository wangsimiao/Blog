title: 基于Ubuntu 14.04的日常开发环境折腾
date: 2016-01-23 22:41:20
categories:
tags:
---

从上大学开始，就开始零零碎碎地接触Linux系统，从大一开始我装了不下10次ubuntu，折腾了一段时间之后又放弃用回了windows，这跟我写博客的经历有点像，很多东西需要一个契机，然后才能发生彻底的改变。这个契机就是在2015年暑假到豆瓣实习，当时我虽然主要从事的是Android开发，但是出于热情以及豆瓣完善的python基础设施，我开始研究python，同事的电脑都是OSX，实习之前脑袋一热掏钱买了台最新的Thinkpad T450s，性能自然没得说，但看到同事都用Mac心里还是有点后悔的，扯远了，说到豆瓣的基础设施，很多都是基于*nix的，在windows下我也折腾过类似mingw或者cygwin之类的东西，但是用着实在不爽，后面干脆就彻底抛弃了windows，装了ubuntu 14.04，发现开发Android也爽多了，Terminal真是各种爽啊，以及其他各种工具的搭建都是十分方便，于是再也不用win了（除了有时候切回去打炉石。。。）。

想来还是把这些记录一下，一方面是做个笔记方便以后查看，另外一方面也可以给想ubuntu开发环境的通过一个参考。

<!-- more -->

### 安利下ubuntu的优点：
- 一个流畅的linux桌面，可以自己定制各种效果，媲美OSX
- 我认为最重要的是贴近服务器环境，程序员友好，各种开发环境的搭建都有比较简便的解决方案，不会像 windows下配环境有各种蛋疼的问题（当然如果你想做.net之流另说）
- 远离各种国产流氓软件，同时没有了各种游戏，能让你更专注于工作
- 当然还有就是成本低，配置一般的电脑均可安装

仅供参考，下面是我的 ubuntu 桌面:
![](/image/1453705459339.png)

![](/image/1453706763250.png)



## 一. 安装篇
- Ubuntu 14.04 LTS live CD制作启动盘
- 建议拿出至少30G的空间，分区什么的网上都有教程，我比较省事，一个交换分区和+主分区搞定了
- 个人推荐 windows 和 ubuntu 双系统，或者 ubuntu + windows虚拟机，以应付一些不时之需（网银，企业网站等）
- 具体安装流程就是U盘启动安装后一路next下去就行了




## 二. 日常软件篇

### 系统配置工具
介绍几个配置系统的GUI工具:
- 自带系统配置：基本满足日常的系统设置
- `unity tweak tool`：升级版的系统设置
- `ubuntu tweak`：貌似是国产软件，有类似一件垃圾清理的功能，功能大部分和 unity tweak tool 重复
- `compiz `：定制各种桌面特效，由于权限比较大经常把桌面搞崩了，这时候下面这个**重置unity桌面配置**的解决方案就派上用场了
>// terminal输入:
dconf reset -f /org/compiz/ 
setsid unity

### Terminal 配置
在ubuntu下一个好的Terminal能够数倍提升工作效率，在本次折腾当中，terminal的配置是花了我最多时间的，最终效果如下：
![](/image/1453707411276.png)

#### oh-my-zsh
zsh是一个扩展的bash，比bash好用不只一点点，[oh-my-zsh](http://ohmyz.sh/)是zsh之上的一个开源配置，包含了各种插件和主题，安装和配置过程[文档](https://github.com/robbyrussell/oh-my-zsh/wiki)里面都很详细了，在这里不赘述。

主要优点如下：

- 智能跳转，配合`autojump`插件，基本不需要输入`cd`，自动定位到你最经常去的目录
- 智能补全，大小写自动纠正，触发补全只需要按一下或两下 tab 键，补全项可以使用 ctrl+n/p/f/b上下左右切换。比如你想杀掉 java 的进程，只需要输入 kill java + tab键，如果只有一个 java 进程，zsh 会自动替换为进程的 pid，如果有多个则会出现选择项供你选择。ssh + 空格 + 两个tab键，zsh会列出所有访问过的主机和用户名进行补全
- 特色主题，实时显示 git 状态
- 各种插件支持，[插件一览](https://github.com/robbyrussell/oh-my-zsh/wiki/Plugins-Overview)

#### tmux
ubuntu自带的terminal并没有支持分屏，tab也不是很好用，我使用[tmux](https://tmux.github.io/)作为软件分屏工具，通过快捷键快速创建会话和窗口，还有一大优点是会话detach后即使用户注销后还可以重新恢复。这里有一份快捷键速查表[tmux cheatsheet](https://gist.github.com/MohamedAlaa/2961058)

#### vim 之 spf13 懒人配置
terminal下自然离不开vim的使用，关于vim的配置估计能写本书了，沿袭了一贯的懒人作风，我使用了最近很火的 [spf13](http://vim.spf13.com/) 配置，这个方案基本一键解决了基本的vim配置。

个人其实不是很推荐 spf13 默认的 solorized 主题，注意如果你想要的 Terminal 的vim 中使用 Solorized 主题的话，你还需要为你的Terminal安装 Solorized 主题，[安装方法](http://www.if-not-true-then-false.com/2012/solarized-linux/#respond)。

上张我的 vim 配置好 spf13 的图：
![](/image/1453723642430.png)


### 开发工具
#### Sublime Text 3
作为 windows 时代的忠实伴侣，在 ubuntu 上的体验却不怎么好，主要是由于 sublime 众所周知的大bug——不能输入中文，虽然网上有了解决输入法的[兼容方案](http://blog.csdn.net/tao_627/article/details/45126047)，但是该方案仍然存在问题：
1. 只有显式指定了兼容库启动才能正常使用输入法，单击图标启动就不行了
2. 当使用兼容库启动时，菜单栏中的一些选项点击后会卡死，比如 `Browse Package `，terminal 插件也无法使用

当然 sublime 应付大部分的编辑工作还是没有问题的，不过，既然我们都到 linux了，为什么不用vim呢？

#### IDEA 一家子
1. Android 开发之 [Android Studio](http://developer.android.com/sdk/index.html)，官方推荐的IDE，亲测在ubuntu下启动比windows快得多，无卡顿，编译速度也提升不少。
2. python 开发之  [PyCharm](https://www.jetbrains.com/pycharm/)，很好用，但是怎么说，也许是 IDE 帮你做得太多了，用着总感觉不爽
3. 前端开发之 [WebStorm](https://www.jetbrains.com/webstorm/)


#### 望而却步的 Emacs
作为一名编辑器折腾狂，没有接触过编辑器之神 Emacs 那是不应该的，相比与 vim 的 spf13 配置，Emacs 也有类似的整套解决方案——[Prelude](https://github.com/bbatsov/prelude)，功能十分全，也是支持插件扩展的。

然而，
个人觉得 Emacs 操作系统上最好的编辑器还是 evil  （逃。。。


### 日常软件
#### 输入法
输入法我折腾过 `谷歌拼音输入法` 和 `搜狗拼音输入法`，这里要吐槽下，谷歌拼音的联想完全不能用，常用词也经常找不到，所以还是墙裂建议使用 [搜狗拼音](http://pinyin.sogou.com/linux/)。

注意：搜狗拼音是基于fctix的，但是千万别遵循网上某些教程说的把`iBus`删除了，如果删了，ubuntu每次启动的时候都会报错，应该是某些组件有依赖。安装搜狗后，只需要将系统输入方式改成 fcitx 就够了。

![](/image/1453724296535.png)

#### 印象笔记+马克飞象
- 印象笔记并没有  linux 版本，但是chrome可以把[网页版](https://www.yinxiang.com/)的保存成网页应用，这样每次点击的时候就可以打开新窗口运行，和原生应用区别也不大。
![](/image/1453726895129.png)
![](/image/1453727161924.png)


- [马克飞象](https://maxiang.io)是一个支持markdown编辑的印象笔记编辑器，由国人制作，是付费软件但是个人觉得还是蛮值的，日常记笔记同步笔记十分方便，本文就是使用马象进行编辑
![](/image/1453727224744.png)


#### IM 解决方案
-  QQ：关于QQ在ubuntu上的安装网上有无数的博客，我基本都一一尝试了，然后得出结论，到目前(`2016.1.25`)为止，最好用的 QQ 解决方案是这个 [linux QQ国际版安装](http://blog.csdn.net/yuan1164345228/article/details/20449459) ，即使是最好用的版本，还是存在很多问题:
    - 漫游记录无法使用，只能保存本地的
    - 文件传输经常失败
    - 视频就别想用了
    - 主界面隐藏后就再也没法调出了，我的解决方案是：QQ放在一个单独的工作区，然后开启`始终保持在其他窗口前端`选项，这样就不会有任何窗口覆盖QQ主界面了

![](/image/1453725551959.png)

最后吐槽下，linux下最好用的 QQ 都这样你敢信？

- Slack：如果你们的团队支持，我是强烈推荐使用Slack的，功能，体验都是一流的，主要是跟 github，CI，trello 等连接后功能变得十分强大。

- Skype：不用说了，老牌IM，豆瓣内部也在使用，但是我们已经开始逐步过渡到 Slack 。然后 ubuntu 版本的体验比较渣。

#### 办公软件 WPS
ubuntu 自带了全套 LibreOffice，但是对 MS Office文件的兼容惨不忍睹，所以还是推荐使用良心国产软件 [WPS](http://community.wps.cn/download/)，界面精良，基本能够满足日常的办公软件需求。




## 三. 个人配置篇

### capslock键映射为control键
此处为emacs党福音，将不常使用的capslock键映射成control，告别扭曲的小拇指：
1. 打开dash，查找`启动应用程序`，添加开机启动项
2. 单击`添加`，名称自定，命令为`setxkbmap -option ctrl:nocaps`
3. 重启系统完成设置


### 关闭USB移动设备的自动弹出
这个比较难找，记录一下：系统设置->详细信息->勾选介质插入时不提示或启动程序
![](/image/1453706618541.png)


## 四. 最后
折腾了这么多，还是想忠告大家一句，如果钱够的话，还是上 Mac 吧。。。





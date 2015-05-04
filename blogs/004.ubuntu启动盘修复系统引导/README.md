#ubuntu启动盘修复系统引导
``linux`` 

今天为实验室的电脑安装了双系统，昨天安装ubuntu win7双系统时由于使用了错误的“新建分区表”选项，导致整个电脑的硬盘被格式化，win7也不复存在，所以只好先安装Ubuntu12.04，再安装win7。
 
为ubuntu分了52G左右的空白磁盘容量，分区如下：
```
swap　　 —— 2G　　　　// 交换分区大小视主机内存而定
/boot　　—— 128M
/  　 　 —— 50G　　　　// 根目录
```

ubuntu安装完成后再U盘安装win7，结果win7直接覆盖了MBR导致ubuntu无法引导，
win7下使用EasyBcd 自动、手动方式均无法修复（通常情况下用EasyBcd即可修复，这里尚存在疑问？）

easybcd能够出现grub但是只剩下一个光标，也就是未找到ubuntu的引导

于是使用 ubuntu启动U盘 进入试用系统修改设置的方法来进行修复，过程如下：

```
sudo fdisk -l  //找到ID为83 的分区那是你的启动分区，记下所有ID为83的分区

// 如果分区中有/boot分区，则在修复引导项<第1步修复Ubuntu引导项>时也要将/boot分区挂载，
如/分区为/dev/sda1，/boot分区为/dev/sda2，则要依次执行

// 以下为挂载操作，目的是使grub能够正确找到启动引导从而成功修复

sudo mount /dev/sda6 /mnt
sudo mount /dev/sda1 /mnt/boot


// 重建MBR

sudo grub-install --root-directory=/mnt /dev/sda  

// 最后执行，更新grub;

sudo update-grub
```
重启后直接进入grub2，其中可以找到所有能够引导的系统，grub2强大到几乎能够找到所有的系统引导。　　

开始时未进行红色两步的操作，导致重启进入grub后显示不了启动项。

####总结
ubuntu硬盘安装时将grub写入了MBR，win7的安装又覆盖了MBR,用ubuntu的启动盘修复启动进入硬盘ubuntu再进行重建MBR。

总而言之还是grub引导比较强大，而且U盘中的Ubuntu试用系统可以看做是装在U盘中的PE修复系统，分区工具也一应俱全，所以果断将U盘做成Ubuntu启动盘兼数据盘。

---
*2015-05-04*
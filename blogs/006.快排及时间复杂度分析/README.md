#快排及时间复杂度分析
``算法``

##一、怎么写快排
快排是分治思想的典型运用，写法也有很多种
####普通青年
```C
int partition(int A[], int l, int r) {
    int privot = A[l];
    while (l < r) {
        while (l < r && A[r] > privot) r--;
        if (l < r)
            A[l++] = A[r];
        while (l < r && A[l] < privot) l++;
        if (l < r)
            A[r--] = A[l];
    }
    A[r] = privot;
    return r;
}

void qsort(int A[], int l, int r) {
    if (l < r) {
        int m = partition(A, l, r);
        qsort(A, l, m - 1);
        qsort(A, m + 1, r);
    }
}
```
####文艺青年
```C
void qsort(int A[], int l, int r)
{
    if (l >= r) return ;

    int m = l - 1;
    for (int i = l; i <= r; i++)
        if (A[i] <= A[r])
            swap(A[++m], A[i]);

    qsort(A, l, m - 1);
    qsort(A, m + 1, r);
}
```
####2B青年
```C++
#include <algorithm>
void main()
{
    std::sort(list.begin(),list.end(),cmp);
}
```
####装逼青年
```haskell
qsort [] = []
qsort (x:xs) = qsort left ++ [x] ++ qsort right
    where left = [y|y<-xs, y<x]
          right = [y|y<-xs, y>=x]
```
```
qsort([]) -> [];
qsort([H | T]) -> qsort([X || X <- T, X < H ]) ++ [H] ++ qsort([X || X <- T, X >= H]).
```

*注:引自[知乎](http://www.zhihu.com/question/24361443)*

##二、时间复杂度分析
学过数据结构都知道快排的平均时间复杂度是O(nlogn),最坏情况下是O(n^2),但是怎么分析呢
####简单分析
由于快排是个分治递归算法，简单画下递归树。

![Screenshot](https://raw.githubusercontent.com/yimun/Blog/master/blogs/006.快排及时间复杂度分析/tree.png)

在最好情况下，每次递归的划分都是1/2，这时的递归树近似为一棵**满二叉树**，数的高度（层数）为log2n，容易简单的判断出在每一层上总共都进行了n次操作，所以时间复杂度是O(nlogn)；在最坏情况下（数组已经有序），这时候递归树是一棵单边树，高度为n，所以时间复杂度是O(n^2)。

####数学帝分析
*注:引自[cnblogs](http://www.cnblogs.com/javawebsoa/p/3194015.html)*


对数据Data = { x1, x2... xn }：
T（n）是QuickSort（n）消耗的时间；
P（n）是Partition(n)消耗的时间；
（Partition专指把n个数据分为大小2份的时间）

![Screenshot](https://raw.githubusercontent.com/yimun/Blog/master/blogs/006.快排及时间复杂度分析/math.png)

有些文章给出了快排的精确计算结果：

![Screenshot](https://raw.githubusercontent.com/yimun/Blog/master/blogs/006.快排及时间复杂度分析/f.png)




---
*2015-05-05 09:34*
title: 论Android后台Service的持久性
date: 2015-10-16 15:20:39
categories:
- Android开发
tags:
- Android
---

## 零
>[Android 中的 Service 全面总结](http://www.cnblogs.com/newcj/archive/2011/05/30/2061370.html)

> - service分为local service（主进程运行）和remote service（单独进程运行）

> - local service和thread都运行在主进程中，他们的主要区别是：当一个Activity被销毁时，thread可能还在运行而其他activity无法得到这个thread的引用，
导致其变成一个幽灵线程不受控制，但是service可以通过intent机制在四大组件里被操作

在Android应用的开发过程中，我们经常需要利用Service在后台做一些持久性的操作，比如推送服务，由于国内没有Google 的GCM统一推送服务，许多独立应用都开发了自己的后台推送Service，但是在Android设备上，这些服务经常因为各种各样的原因意外结束，导致推送机制的失效，那么，研究通过一定手段来保证推送Service在后台的持久运行，对于应用的推送功能稳定性具有重大的意义。

以下是几种可行的方式：


## 一、使用广播唤起
当应用服务遭到意外终止时，通过`BroadcaseReceiver`接收广播重新唤起服务。

几个可以用来作为定期检测Service状态的系统广播：

* `android.intent.action.TIME_TICK`
    - 需要**动态注册**，每一分钟系统发送一次，间隔最稳定
    - 一般在Application中注册使用
    - 缺点是应用销毁后无效

* `android.net.conn.CONNECTIVITY_CHANGE`
    - 检测手机网络状态的改变（如移动数据到wifi状态）
    - 使用该广播唤起推送服务的应用有招行App，微信，QQ等
    - 缺点：广播间隔不够稳定
    - 个人觉得这种方式最好，因为可以结合网络状态改变推送策略，如3G网时的询问间隔应该大于wifi状态的询问间隔

* `android.intent.action.SCREEN_ON`、`android.intent.action.SCREEN_OFF`、`android.intent.action.USER_PRESENT`
    - 和屏幕状态有关的广播
    - 据说在3.0以上版本中，这个广播会在应用完全关闭的情况下被自动屏蔽

以上广播方式存在的问题是；有些手机可以通过订制ROM或者第三方应用，如360手机助手、MyAndroidTools等 **禁用应用的系统广播接收** ，另外，**Android3.0以上的版本中，当应用未曾启动或者进程被完全杀掉后也无法接收广播**    ，因此以上方法可能会不起作用。


## 二、CoreService双服务守护

采用双服务的方式，有`MainService`（推送服务）和`CoreService`（守护服务），能够在一定程度上解决服务被杀的问题。

* 首先给service设置单独进程

```xml
 <service
        android:name=".MainService"
        android:process=":ServiceProcess"
        ></service>
 <service
        android:name=".CoreService"
        android:enabled="true"
        android:process=":ServiceProcess"
        android:exported="true" >
        </service>
```

做法是将UI主进程和service进程隔离开来，通常来说，service进程的内存开销是比较小的，如果在默认不指定，Service是附在UI进程运行的，很容易在整体内存占用过大的情况下被一起杀掉。而单独的进程可以有效避免系统的内存回收。

参考 [Android中对推送服务的优化考虑](http://blog.simophin.net/?p=903)

* 新建一个轻量级的CoreService作为守护,主要用于唤醒进程

```java
public class CoreService extends Service {
    private static final String TAG = CoreService.class.getSimpleName();

    @Override
    public IBinder onBind(final Intent intent) {
        Logger.d(TAG, "onBind()");
        return null;
    }

    @Override
    public void onCreate() {
        super.onCreate();
        Logger.d(TAG, "onCreate()");
        keepMeAlive();
    }

    @Override
    public void onDestroy() {
        Logger.d(TAG, "onDestroy()");
        super.onDestroy();
    }

    @Override
    public int onStartCommand(final Intent intent, final int flags, final int startId) {
        // send status notice
//        IntentHandler.sendStatusNoticeToAll(this);
        this.startService(new Intent(this,MainService.class));
        Logger.d(TAG, "onStartCommand");
        return START_STICKY;
    }

    public void keepMeAlive() {
        // check every two hour to start process
        final long now = System.currentTimeMillis();
        final long intervalMillis = 1000*30;
        final long triggerAtMillis = now + intervalMillis;
        final Intent intent = new Intent(this, CoreService.class);
        final PendingIntent operation = PendingIntent.getService(this, 0, intent,
                PendingIntent.FLAG_UPDATE_CURRENT);
        final AlarmManager am = (AlarmManager) getSystemService(ALARM_SERVICE);
        am.setRepeating(AlarmManager.RTC_WAKEUP, triggerAtMillis, intervalMillis, operation);
    }
}
```

由于CoreService基本为空，被清理的可能性大大降低，`CoreService`对于`MainService`起到守护的作用：

- 当MainService被杀而CoreService依然存活时，CoreService能够自动唤起MainService

- 当两者都被杀时，在CoreService的keepMeAlive方法中，利用AlarmManager进行定时处理，每隔一段时间唤醒当前进程，能够在预定时间间隔内唤起CoreService

------
以上的方法在很大程度上提高了Service的存活率，然而即便使用了这些方法，面对清理助手或是订制ROM的省电功能，服务还是可能会被完全杀掉（目前没有应用的服务能够做到完全存活，微信也是），解决这个问题的方法只能是让用户主动把应用加入的清理的白名单，否则一切还是徒劳。



附：
------
### Android应用接收广播

#### 静态注册 

| 静态注册     | *正常运行* | *已结束，进程缓存*（能找到进程）| *系统清理*（找不到进程）| *猎豹清理*（找不到进程）|
|--------------|------------|---------------------------------|-------------------------|-------------------------|
|*发送系统广播*|    能      |        能                       |    能                   |      不能               |
|*用户定义广播*|    能      |        能                       |    能                   |      不能               |

#### 动态注册

| 动态注册     | *正常运行* | *已结束，进程缓存*（能找到进程）| *系统清理*（找不到进程）| *猎豹清理*（找不到进程）|
|--------------|------------|---------------------------------|-------------------------|-------------------------|
|*发送系统广播*|    能      |        能                       |    不能                 |      不能               |
|*用户定义广播*|    能      |        能                       |    不能                 |      不能               |


但是，使用MyAndroidTools发现，有些系统ROM会**自动检测**唤醒频率高的静态注册广播（用户和系统），并**屏蔽**之








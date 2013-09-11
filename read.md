搜狐面试题
-------------
###题目
请设计一个系统，自动完成对于手机搜狐(http://m.sohu.com/ )系统可靠性的检测。具体要求：

1. 定时递归检测所有m.sohu.com域名的页面以及这些页面上的链接的可达性，即有没有出现不可访问情况。
2. m.sohu.com域名页面很多，从各个方面考虑性能优化。
3. 对于错误的链接记录到日志中，日志包括：连接，时间，错误状态等。
4. 考虑多线程的方式实现

###我的思路

1. 写一个爬虫，提取手机搜狐页面的链接，然后加入队列。
2. 分析这些获得链接。如果能够打开，再提取其中的链接。如果不可达，那么记录错误信息到日志中。

###遇到的困难

1. 链接的分析。在`href=""`中的不一定都是网页链接，可能是.jpg或.css，也可能是javascript的链接。所以要根据需求进行过滤。
2. 多线程的使用。

###可以改进的地方。
后来看到了两篇文章，[用python爬虫抓站的一些技巧总结](http://www.pythonclub.org/python-network-application/observer-spider)和[用Python抓网页的注意事项](http://blog.raphaelzhang.com/2012/03/issues-in-python-crawler/)，给我一些提示。  

1. 网页编码问题。charset有utf-8、gb2312和gbk。
2. 网站仅限浏览器访问时，需要在请求中加入headers信息来伪装。
3. 定时问题。最开始没有看到这个要求，看到时想起《Python Cookbook》讲过可以使用sched模块来执行定时任务。


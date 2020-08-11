#### Django开始

##### 1.创建项目

```shell
django-admin startproject 项目名称
```

##### 2.创建应用

```shell
python manage.py startapp 应用名
```

##### 3.运行项目

```shell
python manage.py runserver
python manage.py runserver 0.0.0.0:80
python manage.py runserver 8888
```

##### 4.视图和 URL 配置

在先前创建的 HelloWorld 目录下的 HelloWorld 目录新建一个 views.py 文件，并输入代码：

**HelloWorld/HelloWorld/views.py 文件代码：**

from django.http import HttpResponse  def hello(request):    return HttpResponse("Hello world ! ")

接着，绑定 URL 与视图函数。打开 urls.py 文件，删除原来代码，将以下代码复制粘贴到 urls.py 文件中：

**HelloWorld/HelloWorld/urls.py 文件代码：**

from django.conf.urls import url  from . import views  urlpatterns = [    url(r'^$', views.hello), ]

整个目录结构如下：

```
$ tree
.
|-- HelloWorld
|   |-- __init__.py
|   |-- __init__.pyc
|   |-- settings.py
|   |-- settings.pyc
|   |-- urls.py              # url 配置
|   |-- urls.pyc
|   |-- views.py              # 添加的视图文件
|   |-- views.pyc             # 编译后的视图文件
|   |-- wsgi.py
|   `-- wsgi.pyc
`-- manage.py
```

完成后，启动 Django 开发服务器，并在浏览器访问打开浏览器并访问：

![img](https://www.runoob.com/wp-content/uploads/2015/01/BD259D4C-2DBE-4657-8761-D8C3508E8A94.jpg)

我们也可以修改以下规则：

**HelloWorld/HelloWorld/urls.py 文件代码：**

from django.urls import path  from . import views  urlpatterns = [    path('hello/', views.hello), ]

通过浏览器打开 **http://127.0.0.1:8000/hello**，输出结果如下：

![img](https://www.runoob.com/wp-content/uploads/2015/01/344A94C7-8D7D-4A69-9963-00D28A69CD56.jpg)

**注意：**项目中如果代码有改动，服务器会自动监测代码的改动并自动重新载入，所以如果你已经启动了服务器则不需手动重启。

##### 5.path() 函数

Django path() 可以接收四个参数，分别是两个必选参数：route、view 和两个可选参数：kwargs、name。

语法格式：

```python
path(route, view, kwargs=None, name=None)
```

- route: 字符串，表示 URL 规则，与之匹配的 URL 会执行对应的第二个参数 view。
- view: 用于执行与正则表达式匹配的 URL 请求。
- kwargs: 视图使用的字典类型的参数。
- name: 用来反向获取 URL。

Django2. 0中可以使用 re_path() 方法来兼容 1.x 版本中的 **url()** 方法，一些正则表达式的规则也可以通过 re_path() 来实现 。

```python
from django.urls import include, re_path

urlpatterns = [
    re_path(r'^index/$', views.index, name='index'),
    re_path(r'^bio/(?P<username>\w+)/$', views.bio, name='bio'),
    re_path(r'^weblog/', include('blog.urls')),
    ...
]
```
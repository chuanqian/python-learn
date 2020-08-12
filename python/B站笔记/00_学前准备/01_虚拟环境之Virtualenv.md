#### 虚拟环境之Virtualenv

##### 安装 virtualenv ：

virtualenv 是用来创建虚拟环境的软件工具，我们可以通过 pip 或者 pip3 来安装：

```shell
pip install virtualenv
```

##### 创建虚拟环境：

创建虚拟环境非常简单，通过以下命令就可以创建了：

```python
virtualenv [虚拟环境的名字]
```

如果你当前的 Python3/Scripts 的查找路径在 Python2/Scripts 的前面，那么将会使 用 python3 作为这个虚拟环境的解释器。如果 python2/Scripts 在 python3/Scripts 前面，那么 将会使用 Python2 来作为这个虚拟环境的解释器。

##### 进入环境：

虚拟环境创建好了以后，那么可以进入到这个虚拟环境中，然后安装一些第三方包，进入虚拟环境 在不同的操作系统中有不同的方式，一般分为两种，第一种是 Windows ，第二种是 *nix ：

- windows 进入虚拟环境：进入到虚拟环境的 Scripts 文件夹中，然后执行 activate 。

- *nix 进入虚拟环境： source /path/to/virtualenv/bin/activate 一旦你进入到了这个虚拟环境中，你安装包，卸载包都是在这个虚拟环境中，不会影响到外面 的环境。

##### 退出虚拟环境：

  退出虚拟环境很简单，通过一个命令就可以完成： deactivate 。

##### 创建虚拟环境的时候指定 Python 解释器：

在电脑的环境变量中，一般是不会去更改一些环境变量的顺序的。也就是说比如你 的 Python2/Scripts 在 Python3/Scripts 的前面，那么你不会经常去更改他们的位置。但是这时 候我确实是想在创建虚拟环境的时候用 Python3 这个版本，这时候可以通过 -p 参数来指定具体 的 Python 解释器：

```shell
virtualenv -p C:\Python36\python.exe [virutalenv name]
```


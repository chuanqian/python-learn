#### 虚拟环境之virtualenvwrapper

virtualenvwrapper 这个软件包可以让我们管理虚拟环境变得更加简单。不用再跑到某个目录下通 过 virtualenv 来创建虚拟环境，并且激活的时候也要跑到具体的目录下去激活。

##### 安装 virtualenvwrapper ：

1. *nix： pip install virtualenvwrapper 。 
2. windows： pip install virtualenvwrapper-win 。

##### virtualenvwrapper 基本使用：

1. 创建虚拟环境：
 
```shell
 mkvirtualenv my_env
 ```
 
 那么会在你当前用户下创建一个 Env 的文件夹，然后将这个虚拟环境安装到这个目录下。 如果你电脑中安装了 python2 和 python3 ，并且两个版本中都安装了 virtualenvwrapper ， 那么将会使用环境变量中第一个出现的 Python 版本来作为这个虚拟环境的 Python 解释器。
 
2. 切换到某个虚拟环境：
 
 ```shell
 workon my_env
 ```

3. 退出当前虚拟环境：
 
 ```shell
 ​```shell
 ```
 
4. 删除某个虚拟环境：

    ```shell
    rmvirtualenv my_env
    ```

5. 列出所有虚拟环境：

    ```shell
    lsvirtualenv
    ```

6. 进入到虚拟环境所在的目录：

    ```shell
    cdvirtualenv
    ```

##### 修改 mkvirtualenv 的默认路径：

在 我的电脑->右键->属性->高级系统设置->环境变量->系统变量 中添加一个参数 WORKON_HOME ，将这个 参数的值设置为你需要的路径。

##### 创建虚拟环境的时候指定 Python 版本：

在使用 mkvirtualenv 的时候，可以指定 --python 的参数来指定具体的 python 路径

```shell
mkvirtualenv --python==C:\Python36\python.exe hy_env
```


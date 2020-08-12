#### DATABASES数据库设置

默认值：（`{}`空字典）

字典，其中包含要与Django一起使用的所有数据库的设置。它是一个嵌套的字典，其内容将数据库别名映射到包含单个数据库选项的字典。

该[`DATABASES`](https://docs.djangoproject.com/zh-hans/2.2/ref/settings/#std:setting-DATABASES)设置必须配置一个`default`数据库。也可以指定任意数量的其他数据库。

最简单的设置文件是使用SQLite的单数据库设置。可以使用以下配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}
```

连接到其他数据库后端（例如MySQL，Oracle或PostgreSQL）时，将需要其他连接参数。请参阅以下[`ENGINE`](https://docs.djangoproject.com/zh-hans/2.2/ref/settings/#std:setting-DATABASE-ENGINE)设置，以了解如何指定其他数据库类型。此示例适用于PostgreSQL：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

提供了更复杂的配置可能需要的以下内部选项：

##### 1.ATOMIC_REQUESTS

默认值：`False`

进行设置`True`以将每个视图包装在该数据库的事务中。请参阅 [连结事务与HTTP请求](https://docs.djangoproject.com/zh-hans/2.2/topics/db/transactions/#tying-transactions-to-http-requests)。

##### 2.AUTOCMMIT

默认： `True`

将其设置为`False`如果要[禁用Django的事务管理](https://docs.djangoproject.com/zh-hans/2.2/topics/db/transactions/#deactivate-transaction-management)，并实现自己的。

##### 3.ENGINE

默认值：（`''`空字符串）

要使用的数据库后端。内置的数据库后端是：

- `'django.db.backends.postgresql'`
- `'django.db.backends.mysql'`
- `'django.db.backends.sqlite3'`
- `'django.db.backends.oracle'`

您可以通过设置`ENGINE`为标准路径（即`mypackage.backends.whatever`）来使用Django不附带的数据库后端 。

##### 4.HSOT

默认值：（`''`空字符串）

连接到数据库时要使用的主机。空字符串表示本地主机。不适用于SQLite。

如果此值以正斜杠（`'/'`）开头并且您正在使用MySQL，则MySQL将通过Unix套接字连接到指定的套接字。例如：

```shell
"HOST": '/var/run/mysql'
```

如果您使用的是MySQL，并且此值*不是*以正斜杠开头，则假定该值为主机。

如果您使用的是PostgreSQL，则默认情况下（为空[`HOST`](https://docs.djangoproject.com/zh-hans/2.2/ref/settings/#std:setting-HOST)），通过UNIX域套接字（中的“本地”行`pg_hba.conf`）完成与数据库的连接 。如果您的UNIX域套接字不在标准位置，请使用`unix_socket_directory`from 的相同值`postgresql.conf`。如果要通过TCP套接字进行连接，请设置[`HOST`](https://docs.djangoproject.com/zh-hans/2.2/ref/settings/#std:setting-HOST)为“本地主机”或“ 127.0.0.1”（中的“主机”行`pg_hba.conf`）。在Windows上，应始终定义[`HOST`](https://docs.djangoproject.com/zh-hans/2.2/ref/settings/#std:setting-HOST)，因为UNIX域套接字不可用。

##### 5.NAME

默认值：（`''`空字符串）

要使用的数据库的名称。对于SQLite，它是数据库文件的完整路径。指定路径时，即使在Windows（例如`C:/homes/user/mysite/sqlite3.db`）上，也始终使用正斜杠。

##### 6.CONN_MAX_AGE

默认： `0`

数据库连接的生存期，以秒为单位。用于`0`在每个请求结束时关闭数据库连接-Django的历史行为-并 `None`用于无限的持久连接。

##### 7.OPTIONS

默认值：（`{}`空字典）

连接到数据库时要使用的其他参数。可用参数取决于您的数据库后端。

有关可用参数的一些信息可以在 [数据库后端](https://docs.djangoproject.com/zh-hans/2.2/ref/databases/)文档中找到。有关更多信息，请查阅后端模块自己的文档。

##### 8.PASSWARD

默认值：（`''`空字符串）

连接数据库时使用的密码。不适用于SQLite。

##### 9.POST

默认值：（`''`空字符串）

连接到数据库时使用的端口。空字符串表示默认端口。不适用于SQLite。

##### 10.TIME_ZONE

默认： `None`

表示此数据库中存储的日期时间的时区的字符串（假设它不支持时区）或`None`。设置的此内部选项[`DATABASES`](https://docs.djangoproject.com/zh-hans/2.2/ref/settings/#std:setting-DATABASES)接受与常规[`TIME_ZONE`](https://docs.djangoproject.com/zh-hans/2.2/ref/settings/#std:setting-TIME_ZONE)设置相同的值 。

这允许与将日期时间存储在本地时间而不是UTC的第三方数据库进行交互。为避免DST更改引起的问题，请勿为Django管理的数据库设置此选项。

如果[`USE_TZ`](https://docs.djangoproject.com/zh-hans/2.2/ref/settings/#std:setting-USE_TZ)是`True`，并且数据库不支持时区（例如SQLite，MySQL，Oracle），则Django会根据此选项（如果设置了该选项）在本地时间读写日期时间，如果不设置，则在UTC中读写日期时间。

如果[`USE_TZ`](https://docs.djangoproject.com/zh-hans/2.2/ref/settings/#std:setting-USE_TZ)为is `True`并且数据库支持时区（例如PostgreSQL），则设置此选项是错误的。

如果[`USE_TZ`](https://docs.djangoproject.com/zh-hans/2.2/ref/settings/#std:setting-USE_TZ)为`False`，则设置此选项是错误的。

##### 11.DISABLE_SERVER_SIDE_CURSORS

默认值：`False`

`True`如果要通过禁用服务器端游标，请将其 设置为[`QuerySet.iterator()`](https://docs.djangoproject.com/zh-hans/2.2/ref/models/querysets/#django.db.models.query.QuerySet.iterator)。[事务池和服务器端游标](https://docs.djangoproject.com/zh-hans/2.2/ref/databases/#transaction-pooling-server-side-cursors) 描述了用例。

这是特定于PostgreSQL的设置。

##### 12.USER

默认值：（`''`空字符串）

连接到数据库时要使用的用户名。不适用于SQLite。

##### 13.TEST

默认值：（`{}`空字典）

测试数据库设置字典；有关创建和使用测试数据库的更多详细信息，请参阅[测试数据库](https://docs.djangoproject.com/zh-hans/2.2/topics/testing/overview/#the-test-database)。

这是测试数据库配置的示例：

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'mydatabaseuser',
        'NAME': 'mydatabase',
        'TEST': {
            'NAME': 'mytestdatabase',
        },
    },
}
```

`TEST`字典中的以下键可用：

**a.CHARSET**

默认： `None`

用于创建测试数据库的字符集编码。此字符串的值直接传递到数据库，因此其格式是后端特定的。

受[PostgreSQL](https://www.postgresql.org/docs/current/multibyte.html)（`postgresql`）和[MySQL](https://dev.mysql.com/doc/refman/en/charset-charsets.html)（`mysql`）后端支持。

**b.COLLATION**

默认： `None`

创建测试数据库时要使用的排序规则。此值直接传递到后端，因此其格式是特定于后端的。

仅`mysql`后端支持（有关详细信息，请参见[MySQL手册](https://dev.mysql.com/doc/refman/en/charset-charsets.html)）。

**c.DEPENDENCIES**

默认值：`['default']`，适用于除以外的所有数据库`default`，该数据库没有依赖关系。

数据库的创建顺序依赖性。有关详细信息，请参见有关[控制测试数据库的创建顺序](https://docs.djangoproject.com/zh-hans/2.2/topics/testing/advanced/#topics-testing-creation-dependencies)的文档。

**d.MIRROR**

默认： `None`

测试期间该数据库应镜像的数据库别名。

存在此设置是为了测试多个数据库的主/副本（在某些数据库中称为主服务器/从服务器）配置。有关详细信息，请参阅有关[测试主/副本配置](https://docs.djangoproject.com/zh-hans/2.2/topics/testing/advanced/#topics-testing-primaryreplica)的文档 。

**e.NAME**

默认： `None`

运行测试套件时要使用的数据库的名称。

如果`None`SQLite数据库引擎使用默认值（），则测试将使用内存驻留数据库。对于所有其他数据库引擎，测试数据库将使用名称。`'test_' + DATABASE_NAME`

请参阅[测试数据库](https://docs.djangoproject.com/zh-hans/2.2/topics/testing/overview/#the-test-database)。

**f.SERIALIZE**

布尔值，用于控制默认测试运行程序在运行测试之前是否将数据库序列化为内存中的JSON字符串（用于在没有事务的情况下恢复测试之间的数据库状态）。`False`如果没有任何带有[serialized_rollback = True的](https://docs.djangoproject.com/zh-hans/2.2/topics/testing/overview/#test-case-serialized-rollback)测试类，可以将其设置为加快创建时间。

**g.TEMPLATE**

这是特定于PostgreSQL的设置。

从中创建测试数据库的[模板](https://www.postgresql.org/docs/current/sql-createdatabase.html)（例如`'template0'`）的名称。

**h.CREATE_DB**

默认： `True`

这是Oracle特定的设置。

如果将其设置为`False`，则测试表空间将不会在测试开始时自动创建，也不会在测试结束时自动删除。

**i.CRATE_USER**

默认： `True`

这是Oracle特定的设置。

如果将其设置为`False`，则不会在测试开始时自动创建测试用户，并在测试结束时自动将其删除。

**j.USER**

默认： `None`

这是Oracle特定的设置。

连接到运行测试时将使用的Oracle数据库时使用的用户名。如果未提供，则Django将使用。`'test_' + USER`

**k.PASSWORD**

默认： `None`

这是Oracle特定的设置。

连接到运行测试时将使用的Oracle数据库的密码。如果未提供，Django将生成一个随机密码。

**l.ORACLE_MANAGED_FILES**

Django 2.2的新功能。

默认值：`False`

这是Oracle特定的设置。

如果设置为`True`，将使用Oracle托管文件（OMF）表空间。 [`DATAFILE`](https://docs.djangoproject.com/zh-hans/2.2/ref/settings/#std:setting-DATAFILE)并且[`DATAFILE_TMP`](https://docs.djangoproject.com/zh-hans/2.2/ref/settings/#std:setting-DATAFILE_TMP)将被忽略。

**m.TBLSPACE**

默认： `None`

这是Oracle特定的设置。

运行测试时将使用的表空间的名称。如果未提供，则Django将使用。`'test_' + USER`

**n.TBLSPACE_TMP**

默认： `None`

这是Oracle特定的设置。

运行测试时将使用的临时表空间的名称。如果未提供，则Django将使用。`'test_' + USER + '_temp'`

**o.DATAFILE**

默认： `None`

这是Oracle特定的设置。

用于TBLSPACE的数据文件的名称。如果未提供，则Django将使用。`TBLSPACE + '.dbf'`

**p.DATAFILE_TMP**

默认： `None`

这是Oracle特定的设置。

用于TBLSPACE_TMP的数据文件的名称。如果未提供，则Django将使用。`TBLSPACE_TMP + '.dbf'`

**q.DATAFILE_MAXSIZE**

默认： `'500M'`

这是Oracle特定的设置。

允许DATAFILE增大到的最大大小。

**r.DATAFILE_TMP_MAXSIZE**

默认： `'500M'`

这是Oracle特定的设置。

允许DATAFILE_TMP增大到的最大大小。

**s.DATAFILE_SIZE**

默认： `'50M'`

这是Oracle特定的设置。

DATAFILE的初始大小。

**t.DATAFILE_TMP_SIZE**

默认： `'50M'`

这是Oracle特定的设置。

DATAFILE_TMP的初始大小。

**u.DATAFILE_EXTSIZE**

默认： `'25M'`

这是Oracle特定的设置。

需要更多空间时扩展DATAFILE的数量。

**v.DATAFILE_TMP_EXTSIZE**

默认： `'25M'`

这是Oracle特定的设置。

需要更多空间时，DATAFILE_TMP的扩展量。
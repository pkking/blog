Title:How to use gitcafe build a blog

##pelican
pelican是基于python的静态web站点生成器

- 详见[pelican](http://docs.getpelican.com/)，本文基于pelican 3.5.0版本
- [源码](https://github.com/getpelican/pelican)
- 特性：
    - 支持markdown和rst
    - 支持主题（比起jekyll的ruby，更熟悉python）
    - 支持插件
    - 代码高亮

##gitcafe pages
gitcafepages是用于显示html文档的，可以用于托管个人博客，容量不限，并且可以连接自己的域名

###WHY gitcafe
github大法好，不过国内的访问速度令人蛋碎，当然，如果是海外党，可能恰好相反，不过如果有米，当然最好能够买一个域名，然后通过CNAME将国外和国内IP分别导到github pages和gitcafe pages，具体做法可以参见[该文](https://ruby-china.org/topics/18084)

##QuickStart
1. 在centos 7下，首先安装python，pip，virtualenv（可选）

        yum install -y python python-devel python-libs python-pip
1. 随后安装pelican和markdown库，如果需要建立虚拟环境(virtualenv)，则可以参见[该文](https://virtualenv.pypa.io/en/latest)

        pip install pelican markdown

1. 建立一个存放博客的目录，并进入目录，取名'waaagh'（绿皮万岁)
    
        mkdir -p waaagh
        cd waaagh
    
1. QuickStart，运行：
`pelican-quickstart`，根据提示，可以快速生成一个静态页面的生产环境，例如:（输入不支持backspace键，不过输入错误可以在随后生成的`pelicanconf.py`文件中修改，直接按回车则是取默认值）


        (blog)[root@localhost blog]# pelican-quickstart 
        Welcome to pelican-quickstart v3.5.0.
        
        This script will help you create a new Pelican-based website.
        
        Please answer the following questions so this script can generate the files
        needed by Pelican.
        
            
        > Where do you want to create your new web site? [.] .
        > What will be the title of this web site? waaagh!!!
        > Who will be the author of this web site? lichaoran
        > What will be the default language of this web site? [en] zh
        > Do you want to specify a URL prefix? e.g., http://example.com   (Y/n) pkking.github.io
        You must answer 'yes' or 'no'
        > Do you want to specify a URL prefix? e.g., http://example.com   (Y/n) yes
        > What is your URL prefix? (see above example; no trailing slash) pkking
        > Do you want to enable article pagination? (Y/n) y
          How many articles per page do you want? [10] 
        ▽ Do you want to generate a Fabfile/Makefile to automate generation and publishing? (Y/n) y
        > Do you want an auto-reload & simpleHTTP script to assist with theme and site development? (Y/n) y
        > Do you want to upload your website using FTP? (y/N) n
        > Do you want to upload your website using SSH? (y/N) y
        > What is the hostname of your SSH server? [localhost] 
        > What is the port of your SSH server? [22] 
        > What is your username on that server? [root] pkking
        > Where do you want to put your web site on that server? [/var/www] 
        > Do you want to upload your website using Dropbox? (y/N) n
        > Do you want to upload your website using S3? (y/N) n
        > Do you want to upload your website using Rackspace Cloud Files? (y/N) n
        > Do you want to upload your website using GitHub Pages? (y/N) y
        > Is this your personal page (username.github.io)? (y/N) 
        Done. Your new project is available at /root/blog/blog
    

完成后，目录结构如下：
    
     yourproject/
    ├── content
    │   └── (pages)
    ├── output
    ├── develop_server.sh
    ├── fabfile.py
    ├── Makefile
    ├── pelicanconf.py       # Main settings file
    └── publishconf.py       # Settings to use when ready to publish

##push一篇博文
通常，我们将content目录作为存放文章源文件的目录，pelican支持rst，markdown和html文件。
不管3721，先撸一篇markdown文章吧：

    Title: My super title
    Date: 2010-12-03 10:20
    Modified: 2010-12-05 19:30
    Category: Python
    Tags: pelican, publishing
    Slug: my-super-post
    Authors: Alexis Metaireau, Conan Doyle
    Summary: Short version for index and feeds
    
    hello world!

接下来，解释一下上面的文件内容：

- 以:隔开的key-value键值对可以成为元素局（metadata），他们构成了一些文章的基础属性，例如日期，标题，摘要等。
- Title为该文的标题，更多的源数据可以参见[这里](http://docs.getpelican.com/en/3.5.0/content.html#file-metadata)，（根据链接中的配置，我在`pelicanconf.py`中添加了`DEFAULT_DATE = 'fs'`行，使文章自动使用了文件系统的mtime作为时间戳。

写好文章后，将其命名为hello_world.md（.md为markdown源文件的后缀名），然后在project根目录运行`pelican /path/to/your/content/ [-s path/to/your/settings.py]`，其中，`/path/to/your/content`即是存放文章源文件的目录，刚才我们使用了content目录，该目录的名称依然可以在`pelicanconf.py`中配置，甚至，配置文件`pelicanconf.py`都可以用其他配置文件代替，只需要指定 `path/to/your/settings.py`即可。

**TIPS**:
同时在`project`目录，命令`make html`也可以直接生成所有的静态页面，不过他会将`output`目录的所有内容先删除，如果没有配置`OUTPUT_RETENTION `，将会删除类似.git一样的版本跟踪文件。因此，可以使用`make regenerate`更新静态页面，同时，可以运行`make serve`来启动一个本地服务器，通过[localhost.com:8000](localhost.com:8000)来访问。命令`make devserver`可以重复上面个两个命令。

##配置pelican
配置文件`pelicanconf.py`包括了众多选项，可以参见[该页](http://docs.getpelican.com/en/3.5.0/settings.html)进行配置

##git端的配置
在生成好第一篇文章后，可以进入到`output`目录，这里的内容就是即将托管到`gitcafe pages`的静态页面，首先，到gitcafe.com建立一个user pages或者project pages，方法参见[官方帮助文档](https://gitcafe.com/GitCafe/Help/wiki/Pages-%E7%9B%B8%E5%85%B3%E5%B8%AE%E5%8A%A9#wiki)，简化下来的步骤就是：

1. 在gitcafe.com中建立一个和用户名相同的repo
1. 根据刚建立的空repo首页，将git username和email配置为相应的数据（在github中，非验证邮箱和用户名会导致pages build failure，不知道gitcafe是否有一样的机制）
1. 在`output`目录，依次运行
    
        git init #初始化仓库
        git checkout -b gitcafe-pages #建立制定分支，pages只会渲染该分支中的页面
        git add -A #添加修改
        git commit -m"init the blog" #提交
        git remote add gitcafe git@gitcafe.com:pkking/pkking.git #pkking替换为你的gitcafe用户名
        git push gitcafe gitcafe-pages #将提交push到gitcafe
    
1. OK，一切就绪，访问pkking.gitcafe.io查看渲染好的页面吧

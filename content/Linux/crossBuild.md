Title: 关于在amd64架构下构建arm架构deb包的问题
Tags: ubuntu,sbuild,arm,crossBuild
Date: 2015-05-12 19:37

# poky & yocto
最近项目组在准备开发基于 `arm`的版本，于是涉及到了交叉编译和交叉构建，前者很简单，只需要安装相应的arm-gcc即可。
可惜生活往往不是如此简单，出于某些目的，我们需要构建基于ubuntu 中的源码和包管理机制构建的版本，也就是说，我们需要制作arm版本的ubuntu rootfs，之所以不能直接使用`ubuntu core for arm`，是因为某些时候可能需要修改某些包的源码，所以需要同时搭建一个交叉编译和构建包的环境。

也就是一个 `src -> binary -> package`的过程

### Yocto
记得在实验室的时候，用`bitbake`这个工具编译过arm下的用户态程序，于是google一番发现，bitbake原来是一个叫做Yocto的工具下的一个python写的工具集，用于将源码交叉构建为目标硬件的二进制程序（甚至软件包），遂大喜，下了最新的yocto之后，根据官方的 Quick Start迅速构建了一个img

不过转念一想，既然要基于ubuntu的源码，那么yocto中所带的源码则显然无法使用了，因为yocto虽然也能制作deb包，不过和ubuntu中的版本完全无法兼容，并且ubuntu对上游源码所打的一些补丁yocto也没有集成，因此可能需要对yocto进行一番改造。

### 放弃
参考了yocto的文档后，我们发现，yocto实现deb包的机制和通常的debian/ubuntu构建流程不太一样，后者使用dpkg-buildpackage来构建特定的包，而yocto则采用了自己实现的机制（`lib/pm.py`利用dpkg apt等工具实现了自己的打包流程）这导致其构建包的流程几乎不透明了，而要通过修改yocto来达到生成特定版本ubuntu兼容的deb包，则可以预见包含比较大的工作量。

故此，yocto的路线暂停，而这里的主要问题是，ubuntu的rootfs是一个基于二进制包的img，我们只需要找到一种方法，能够将上游源码构建为某个版本apt能够识别、安装的包即可，有了这些包，构建rootfs就再轻松不过了

# sbuild
在yocto的方案受挫后，我们发现，其主要的问题在于如何将交叉编译生成的二进制文件打包成软件包，经过一番搜索后，cross-build映入了我们眼帘。在看完：

- [这篇](https://wiki.ubuntu.com/CrossBuilding)
- [这篇](https://wiki.linaro.org/Platform/DevPlatform/CrossCompile/CrossBuilding)
- [这篇](https://wiki.linaro.org/Platform/DevPlatform/CrossCompile/CrossbuildingQuickStart)

等文后，总结出一个结论：妈蛋交叉构建还是个坑啊，大家要构建最好把源码传到`launchpad`上啊，我们建议大家构建的时候用最新的工具链哟，也欢迎搭建帮忙一起测试sbuild和那些个坑爹的package 维护者挖的坑 （逃

不过第一篇文中，同时也表示业界在crossbuild的泥潭里正缓慢的前行，那么之前的ubuntu for arm版本又是如何构建出来的呢？？

### crossBuild node
这里就要请出[launchpad](https://launchpad.net/ubuntu)了，根据[这篇文章](http://comments.gmane.org/gmane.linux.embedded.yocto.general/15379)，可以得知，ubuntu基本是采用launchpad的分布式构建结点来制作软件包的，并且他们还是用的最慢的本地构建方法（也就是利用`qemu-static-user`软件包，在amd64的虚拟机上构建arm环境，然后用arm架构的工具构建软件包），事实上，launchpad的[这篇文章]也是这么说的(https://help.launchpad.net/Packaging/PPA)。

既然如此，那我们何不自己搞一发本地构建？

于是跟随者这篇[guide](https://wiki.ubuntu.com/SimpleSbuild) 我们搭建了一个 host,build,target都是armhf的chroot环境（前面的教程搭建的是基于amd64的sbuild chroot，只需要在mk-sbuild和sbuild的时候，将--arch=armhf加入命令行即可），然后就可以轻松的在amd64下构建arm软件包了

# buildd
### 问题
用sbuild构建了一些包之后，发现，我们的日志和launchpad上的build.log并不一样，launchpad似乎使用了一个叫做buildd的工具来进行自动化的构建，google一番之后，发现了[这篇文章](https://www.debian.org/devel/buildd/)，原来launchpad利用`wanna-build buildd sbuild`构建了一套自动化构建环境，buildd周期性的检查upload上来的源码包，而wanna-build则维护了一个包含各个软件包在各个架构上的构建状态的数据库，buildd通过数据库来选择是否重新构建（如果该包当前状态是未成功构建或超过包的保质期）或者忽略本次构建（包已经构建成功并且在保质期内），而最终的构建工具，则是sbuild

### 还是sbuild
最终真相大白，虽然我们可能没有资源架设`openstack集群`来进行分布式构建，但是只要采用和launchpad一样策略：使用sbuild构建各个架构的软件包，也是毫无问题的。

最后，送上利用sbuild从零构建arm等架构软件包的[官方教程](https://wiki.debian.org/sbuild)

# 参考文献：
- https://wiki.debian.org/sbuild
- https://wiki.ubuntu.com/SimpleSbuild
- https://wiki.linaro.org/Platform/DevPlatform/CrossCompile/UsingMultiArch
- https://wiki.ubuntu.com/CrossBuilding
- https://wiki.linaro.org/Platform/DevPlatform/CrossCompile/CrossBuilding
- https://wiki.linaro.org/Platform/DevPlatform/CrossCompile/CrossbuildingQuickStart
- http://comments.gmane.org/gmane.linux.embedded.yocto.general/15379
- https://help.launchpad.net/Packaging/PPA
- https://www.debian.org/devel/buildd/
Title: runc 源码分析-1 概述
Tags: container, oci, rkt, docker, k8s, golang
Date: 2017-05-11 19:00

## runc 是什么
最近在协助其他部门开发基于Android的容器方案，有机会深入接触了下`kernel`，`docker`等项目，发现容器的现状比起我14年刚毕业时，已经大不一样了

- 业界大佬们搞出个 OCI(Open Container Initiative) 标准，避免容器生态和 docker 耦合过紧
- 内核中关于容器的开发也如火如荼，包括 capabilities, fs, net, uevent等和容器相关的子系统，代码增长都迎来了第二春
- 由于OCI的存在，各种容器项目（rkt, docker, OpenVZ)可以更加专注其他方面（security, auto deploy, scale)

同时docker将`libcontainer`贡献给OCI后，OCI基于libcontainer开发了`runc`，runc因此成为了[OCI runtime spec](https://github.com/opencontainers/runtime-spec)的一个官方实现。

## runc 在容器引擎中的位置
docker 为了兼容 OCI runtime spec，在1.11版本后，将runc嵌入到项目中，作为最终管理、操作容器的底层工具集

下图就是runc出现前后，docker架构的变化</br>
![runc-in-docker-engine-process](/images/rkt-vs-docker-process-model.png)

如下图所示，runc在容器引擎中，负责容器生命周期的管理和配置，实际上，runc本身已经具备了容器基本的管理能力，而docker，rkt等高层次的应用，则更加关注于对容器的管理，编排等领域（抢k8s的地盘啊）
![runc-in-docker-arch](/images/runc-in-docker.png)



同时，runc符合 OCI runtime的标准，因此，任何实现了OCI runtime标准的包，都可以替换其在容器引擎中的位置（类似的，k8s最近终于引入了一个兼容层，开始将自己和docker/rkt解耦合，当前docker版本(1.12)中，已经可以通过参数替换oci runtime了）。

## runc的代码结构
如果看一下 runc目录中`.go`文件的名称和`runc help`中 command的名称，可以发现runc代码的目录还是很清晰的，基本每一个`.go`文件，就对应了一个command
```bash
~/runc@master lcr% tree -L 1 
.
├── checkpoint.go
├── contrib
├── CONTRIBUTING.md
├── create.go
├── delete.go
├── Dockerfile
├── events.go
├── exec.go
├── init.go
├── kill.go
├── libcontainer
├── LICENSE
├── list.go
├── main.go
├── MAINTAINERS
├── MAINTAINERS_GUIDE.md
├── Makefile
├── man
├── NOTICE
├── notify_socket.go
├── pause.go
├── PRINCIPLES.md
├── ps.go
├── README.md
├── restore.go
├── rlimit_linux.go
├── run.go
├── script
├── signals.go
├── spec.go
├── start.go
├── state.go
├── tests
├── tty.go
├── update.go
├── utils.go
├── utils_linux.go
├── vendor
├── vendor.conf
└── VERSION
```

后续本文将会逐步进入runc的代码，摸清`runc`运行时的各个方面。

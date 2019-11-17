---
title: runc 源码分析-1 概述
tags: 
- container
- oci
- rkt
- docker
- k8s
- golang
date: 2017-05-11 19:00
---
## runc 是什么
最近在协助其他部门开发基于Android的容器方案，有机会深入接触了下`kernel`，`docker`等项目，发现容器的现状比起我14年刚毕业时，已经大不一样了

- 容器的工业级标准化组织OCI(Open Container Initiative)出炉，这是业界大佬为避免容器生态和`docker`耦合过紧做的努力，也是docker做出的妥协
- 随着docker等容器引擎自身功能越来越丰富，其逐渐呈现出组件化的趋势（将底层交给OCI，自己则专注网络，配置管理，集群，编排，安全等方面）
- 内核中关于容器的开发也如火如荼，包括 capabilities, fs, net, uevent等和容器相关的子系统，代码增长都迎来了第二春

如上所说，随着`libcontainer`从docker引擎中解耦并贡献给OCI后，runc实际上已经成为了第一个[OCI runtime spec](https://github.com/opencontainers/runtime-spec)的实现。
可以说，任何`OCI runtime spec`的实现，都能通过自己是提供的关于容器的接口实现容器的起停，资源管理等功能。

## runc 在容器引擎中的位置
docker为了兼容`OCI runtime spec`，在1.11版本后，将runc与`docker daemon`独立开来，作为实际的管理、操作容器的底层组件。

下图就是runc出现前后，docker架构的变化。</br>
![runc-in-docker-engine-process](/images/rkt-vs-docker-process-model.png)

如下图所示，`runc`在容器引擎中，仅负责容器生命周期的管理和配置（在docker中，受`containerd`调用）；由于runc本身已经具备了容器基本的管理能力，因而docker，rkt等则能更加关注于对容器的网络管理，编排等领域。</br>
![runc-in-docker-arch](/images/runc-in-docker.png)

## runc 的意义
runc符合`OCI runtime spec`，同时目前也一直在社区中进行着维护。
根据OCI的文档，任何实现了`OCI runtime spec`的组件，都可以替换`runc`在容器引擎中的位置，因此，这也可以说是给业界提供了一个Production-Grade的DEMO。（类似的，k8s最近终于引入了一个兼容层，开始将自己和docker/rkt解耦合；另：当前docker版本(1.12)中，也已经可以通过参数替换`oci runtime`了）。

## runc的代码结构
如果看一下 runc目录中`.go`文件的名称和`runc help`中 command的名称，可以发现runc代码的目录还是很清晰的，基本每一个`.go`文件，就对应了一个command
```bash
% tree -L 1 
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

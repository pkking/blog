---
title: 在openEuler中搭建i3wm
tags:
- tiling window manager
- openEuler
- i3
date: 2023-3-18
---

## 什么是i3
一个[平铺式窗口管理器](https://en.wikipedia.org/wiki/Tiling_window_manager)
就像emacs一样，在习惯使用的人手里，i3可以是一个及其有效率的生产力工具
一个介绍视频 https://www.bilibili.com/video/BV1L4411P7zn/?spm_id_from=333.337.search-card.all.click&vd_source=78e28bd49f69d106107f568dc1fa8295
## 最终效果图
![](layout.jpeg)

## 相关软件（包）
[i3wm](https://eur.openeuler.openatom.cn/coprs/mywaaagh_admin/i3wm/)
[vscode](https://code.visualstudio.com/docs/setup/linux)
[neofetch](https://github.com/dylanaraps/neofetch)
[i3config](https://gitee.com/mywaaagh_admin/i3configs)

## HOWTO
1. i3是基于X协议的，因此需要先安装X Server 
    ```bash
    dnf in xorg-x11-server
    ```

1. 同时i3也仅仅是一个window manager，一个完整的linux桌面环境（desktop environment)通常会包含[非常多的组件](https://wiki.archlinux.org/title/desktop_environment#Custom_environments)，因此还需要安装一些基本组件
    ```bash
    dnf in xorg-x11-drv-*  lightdm lightdm-gtk
    ```
1. 最后，我们安装i3相关的组件
    ```bash
    curl -o /etc/yum.repos.d/i3wm.repo -L https://eur.openeuler.openatom.cn/coprs/mywaaagh_admin/i3wm/repo/openeuler-22.03/mywaaagh_admin-i3wm-openeuler-22.03.repo
    dnf in i3 i3status i3blocks i3lock i3blocks-contrib xfce4-terminal xcompmgr acpi dmenu feh
    git clone https://gitee.com/mywaaagh_admin/i3configs && cd i3configs && sh install.sh
    ```
1. 安装完成后，启动`lightdm`
    ```bash
    sudo systemctl start lightdm
    ```
    ![](lightdm.png)

附一些i3的基本操作指令（下面的mod在通常的PC上是win键）
```
mod+d：调出dmenu，用于快速启动进程
mod+enter：启动terminal
mod+↑/mod+↓/mod+←/mod+→：调整focus的窗口
mod+shift+q：关闭当前focus的窗口
mod+shift+r：热加载配置文件
mod+shift+e：关闭i3
mod+shift+l：锁屏
```
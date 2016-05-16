Title:Yocto源码分析
Tags:python,Yocto
Date: 2015-03-11 19:30

## server如何运作

在`bb/server/process.py`中，定义了当Yocto采用多进程`B/S`架构时，`server`进程的启动方式：

- `start_server()`，在`bin/bitbake`中，包含了一个`start_server()`函数，该函数根据命令行参数，实例化相应的`server`对象，并且调用`server`的`detach`函数，这个函数则调用了`server`对象的`start()`函数
- `run()`:在`bb.server.ProcessServer`类中，存在一个`run`函数，该函数设置了一些UI事件，并且调用了`bb.cooker.server_main()`，该函数接受两个参数，第一个是一个cooker实例，第二个是一个可执行的函数，Yocto中将`self.cooker`和`self.main`作为这两个参数，由于`ProcessServer`类继承于`Process`类，因此在调用该类的`start()`方法时，`run()`会被自动调用，因此在调用`server.start()`时，实际调用的是`server_main()`函数
- `server_main()`:该函数执行一些预处理任务（`bb.cooker.pre_serve()`），然后调用传进来的函数并且返回其返回值:

```python
#__file__ = 'bitbake/lib/bb/cooker.py'

def server_main(cooker, func, *args):
	cooker.pre_serve()
	#something else
         ret = func(*args)
	cooker.post_serve()
	return ret
```

而这里的`func`，即是上面传进来的`bb.server.ProcessServer.main`，因此调用`server_main()`实际上是调用了`ProcessServer`类的`main()`函数

- `ProcessServer.main()`:该函数会执行一个重要的`while`循环：

```python
#__file__ = 'bitbake/lib/bb/server/process.py'
def main(self):
    # Ignore SIGINT within the server, as all SIGINT handling is done by
    # the UI and communicated to us
    self.quitin.close()
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    while not self.quit:
        try:
            if self.command_channel.poll(): # 检测是否有命令数据
                command = self.command_channel.recv()
                self.runCommand(command)
            if self.quitout.poll():
                self.quitout.recv()
                self.quit = True
	# 若无数据可读，执行注册的idle命令
            self.idle_commands(.1, [self.event_queue._reader, self.command_channel, self.quitout])
        except Exception:
            logger.exception('Running command %s', command)

	self.event_queue.close()
    bb.event.unregister_UIHhandler(self.event_handle.value)
    self.command_channel.close()
    self.cooker.shutdown(True)
```

在其中不断的从两个管道中读取数据，一个管道为命令管道，这个管道两头连接着`ui`和`server`，这样server就可以接受来自`ui`的命令，并把执行结果返回给`ui`；另一个管道为异常管道，当其他模块在产生不可恢复的异常后，会向这个管道发送`'quit'`消息，接收到该命令后主循环直接退出；在检查完这两个管道后，主循环调用`idle_commands()`，并设置0.1秒的延时，用于等待几个管道的数据

- `idle_commands`：该函数调用`register_idle_function`函数注册的`idle`函数，这个函数在`bb.Command.runCommand()`中，通过
	
```python 
self.cooker.configuration.server_register_idlecallback(self.cooker.runCommands, self.cooker)
```

	这段代码注册，可以看到，注册的函数为`bb.cooker.runCommands`，然后该函数调用这个注册的函数，如果未找到注册函数，则调用`select.select()`等待0.1秒后返回。

- `bb.cooker.runCommands`:该函数就是被注册的idle函数，他会被`server`主循环周期的调用，而该函数的实际内容，则是调用`bb.command.Command.runAsyncCommand`来执行一个已经就绪的异步命令
- `bb.command.Command.runAsyncCommand`:该函数会判断当前cooker从状态，而分别调用`updateCache()`函数或者调用`command`对象的`currentAsyncCommand`成员函数，这个函数会在多种情况下被赋值为某个函数对象和其参数组成的元组`(command, options)`，当该函数被调用时，则会执行在`currentAsyncCommand`注册的函数，而`updateCache()`则会为启动其他的任务，例如`parse`
- `currentAsyncCommand`的赋值：`currentAsyncCommand`只会在`command.runCommand`函数中被赋值，而`command.runCommand`函数，则会在`server`对象的`runCommand()`中被调用，`server.runCommand()`的调用，则出现在`ui`端的`main()`中唯一一次主动调用`server`的代码，这样，即是在`ui`端的`main`函数中，启动了
	
## 依赖关系如何解析
代码位于`bb.runqueue.RunQueueData.prepare()`函数中的注释的`PART A`部分和内嵌函数`generate_recdeps`

## bb文件如何解析
入口位于`bb.cooker.updateCache()`函数中，该函数中有如下代码：

```python
self.parser = CookerParser(self, filelist, masked)
```

这段代码初始化了一个`CookerParser`对象，这个对象的构造函数中，调用了`self.start()`，因此这段代码直接启动了bb文件的解析，具体的`start()`函数代码在`bb/cooker.py`中的`CookerParser`类中

## UI端如何运作

由于在Yocto中，服务进程先于UI启动，因此第一次执行命令需要通过`ui`传递给`server`，而`ui`的入口函数，则是位于`lib/ui/ui_module_name.py`文件中的`main()`函数，根据采用的不同的`ui`模块（默认采用knotty.py），`main`函数有不同的行为，这里以knotty.py中的main作为例子进行分析

- `bb.ui.knotty.main` 这个函数为`ui`端的入口函数，最核心的代码为

```python
	#__file__ = 'bitbake/lib/bb/ui/knotty.py'

	if not params.observe_only:
        params.updateFromServer(server)
        params.updateToServer(server)
        cmdline = params.parseActions()
        if not cmdline:
            print("Nothing to do.  Use 'bitbake world' to build everything, or run 'bitbake --help' for usage information.")
            return 1
        if 'msg' in cmdline and cmdline['msg']:
            logger.error(cmdline['msg'])
            return 1

        ret, error = server.runCommand(cmdline['action'])
        if error:
            logger.error("Command '%s' failed: %s" % (cmdline, error))
            return 1
        elif ret != True:
            logger.error("Command '%s' failed: returned %s" % (cmdline, ret))
            return 1
```

这段代码，通过`params.parseActions()`从用户调用的`bitbake <target>`命令，解析出一个`cmdline`字典，其中的`action`键是一个列表，其中包含了要运行的命令的字符串格式，要构建的目标`<target>`和构建的cmd（默认为`build`），例如:`cmdline[action]=["buildTarget", "zlib", "build"]`，就意味着即将要运行的命令为`buildTarget`，构建目标为`zlib`，cmd为`build`；而`msg`键对应了需要传送给`server`端显示的消息，当命令行参数解析到不合适的内容时，则会发送给服务器结束命令，关闭`ui`和`server`进程。
	如果没有出错，通常的第一个`action`都是`buildTarget`，这个`action`随后被作为参数，传给`bb.server.ServerCommunicator.runCommand()`函数，该函数调用服务端的函数`bb.server.ProcessServer.runCommand`来执行命令
			
- `bb.server.ProcessServer.runCommand`:该函数将上面`action`中的命令数据通过`bb.cooker.command.runCommand()`进行处理，并将返回值通过管道发送给`ui`端，这也是唯一一次`ui`端显式的调用`server`的函数。

- 各种event的处理：在`bb.ui.knotty.main()`中，存在着一个`while`循环，该循环读取服务端的管道，并根据服务端返回的命令执行结果和状态执行相应的代码，或者关闭服务端，或者继续发送命令。

## buildTarget ##
在 `bitbake/bb/cooker.py`中，有一个`buildTarget`函数，该函数为在无任何参数的`bitbake`命令时的服务端入口，例如:

```shell
$ bitbake zlib #target 为 zlib
```

这是服务端会调用`buildTarget`作为如何，该函数如下:

```python
def buildTargets(self, targets, task):
     """
    Attempt to build the targets specified
    """

    def buildTargetsIdle(server, rq, abort):
        msg = None
        if abort or self.state == state.forceshutdown:
            rq.finish_runqueue(True)
            msg = "Forced shutdown"
        elif self.state == state.shutdown:
            rq.finish_runqueue(False)
            msg = "Stopped build"
        failures = 0
        try:
            retval = rq.execute_runqueue()
        except runqueue.TaskFailure as exc:
            failures += len(exc.args)
            retval = False
        except SystemExit as exc:
            self.command.finishAsyncCommand()
            return False

        if not retval:
            bb.event.fire(bb.event.BuildCompleted(len(rq.rqdata.runq_fnid), buildname, targets, failures), self.data)
            self.command.finishAsyncCommand(msg)
            return False
        if retval is True:
            return True
        return retval

    self.buildSetVars()

    taskdata, runlist, fulltargetlist = self.buildTaskData(targets, task, self.configuration.abort)

    buildname = self.data.getVar("BUILDNAME")
    bb.event.fire(bb.event.BuildStarted(buildname, fulltargetlist), self.data)

    rq = bb.runqueue.RunQueue(self, self.data, self.recipecache, taskdata, runlist)
    if 'universe' in targets:
        rq.rqdata.warn_multi_bb = True

    self.configuration.server_register_idlecallback(buildTargetsIdle, rq)
```

可以看到，这个函数做了以下几件事：

1. 定义了一个内嵌函数`buildTargetsIdle`，看名字可以得知，该内嵌函数会作为`idle`函数被注册到`server`中，周期的被调用
2. `self.buildSetVars()`用于设置一些和`BUILDNAME`,`BUILDTIME`等变量
3. `buildTaskData`用于生成任务数据，其中包括`taskdata`，`runlist`，和`fulltargetlist`；其中，`taskdata`是一个`bb.taskdata.TaskData`类的实例，这个对象中包含了和该任务相关的信息，例如依赖，任务名等，`runlist`则是该任务的各个目标的名称和对应的task，并以列表的形式进行存储，例如`["base-files","do_build"]`就代表了目标`base-files`，其task为`do_build`，而`fulltargetlist`则是所有target的列表
4. 通过`rq = bb.runqueue.RunQueue(self, self.data, self.recipecache, taskdata, runlist)`来构造一个`RunQueue`实例，为随后的build工作做好准备
5. 将定义的内嵌函数注册为`idle`回调函数，使其被周期地调用，因此，我们需要分析该函数的实现：

### buildTargetsIdle ###

1. 根据上面的代码，该函数主要执行了`rq.execute_runqueue()`函数，该函数位于`bb/runqueue.py`中，而`execute_runqueue()`又调用了`_execute_runqueue()`，而`_execute_runqueue()`的实际工作，是根据`runqueue`的实际状态，进行不同的行为：

	- 在`runQueuePrepare`态，调用`bb.runqueue.RunQueueData.prepare()`，这个函数是很相当长的函数，主要行为包括：
		1. STEP A:解析出一个需要执行的任务列表，包括解析依赖
		2. STEP B:标记所有需要执行的任务
		3. STEP C:去掉不需要执行的任务
		4. STEP D:检测并确定最终的需要执行的任务列表
		5. 进入`runQueueSceneInit`状态
	- 在`runQueueSceneInit`状态，调用`runqueue.start_worker()`启动，启动工作进程，并构建一个`RunQueueExecuteScenequeue`对象，将状态设置为`runQueueSceneRun`
	- 在`runQueueSceneRun`状态，调用`RunQueueExecuteScenequeue.execute()`，该函数会将准备好的task依次运行，随后，将状态设置为`runQueueRunInit`
	- 在`runQueueRunInit`状态，会构造一个`RunQueueExecuteTasks`对象，然后将状态设置为`runQueueRunning`
	- 在`runQueueRunning`状态，会调用`RunQueueExecuteTasks`对象的`execute()`函数，该函数会执行在上面的`RunQueueData`状态中准备的task，并进入`runQueueCleanUp`状态
	- `runQueueCleanUp`状态，调用`RunQueueExecute.finish()`函数，并将状态设置为`runQueueComplete`
	- `runQueueComplete`状态，销毁worker，然后该函数返回

## 载入cache的入口 ##

入口函数是`bb/cache.py`中的`load_cachefile()`函数

## run.do_xxx 脚本如何生成 ##

在`bb/build.py`中，存在`exec_func`函数，该函数运行的某个函数，将会在`build/tmp/work`中创建`run.do_xxx.pid`名称的脚本，并运行它

## 如何生成image 

yocto在构建完成所有的软件包后，会将所有构建的软件包放在`${TMPDIR}/deploy`目录下，称之为软件源，在启动构建rootfs的活动（名为`do_rootfs`的task）后，将会执行三个函数：

- create_manifest() 构建软件包的manifest用于test image，并且生成一个`package`列表为`create_rootfs()`函数提供需要安装的软件包列表
- create_rootfs() 构建rootfs文件系统，包括执行`pre_cmd`，安装所需软件包，构建/etc ,/dev等目录，构建内核模块，运行ldconfig等，完成rootfs的构建
- create_image 根据image的压缩类型和文件系统类型，制作一个或多个image

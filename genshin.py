# 参考 https://www.v2ex.com/t/962671

# 在正常情况下，原神在切换到后台后，虽然不再占用GPU但仍会占用一定的CPU，导致笔记本风扇狂转
# 没有办法通过打开大地图，切角色界面等游戏内方法消除后台的CPU占用

# 本脚本通过暂停原神的进程，实现切换到后台时消除CPU占用
# 使用本脚本后，原神在后台不会占用CPU，GPU，但仍会占用内存和显存，用以切换到前台快速恢复

# 需要使用管理员权限打开powershell，运行python脚本
# 仅限Windows

import time
import os
import win32process
import win32gui
import psutil
import win32com.client

# process name 需要暂停的进程名
name='YuanShen.exe'
# resume time 每隔10个循环恢复时间，用于防止掉线
resume_time=0.1
# check time 检查是否切换后台的间隔时间
check_time=1

def get_yuanshen_pid():
    try:
        process_name = name
        WMI = win32com.client.GetObject('winmgmts:')
        processes = WMI.InstancesOf('Win32_Process')
        pid = next((process.ProcessId for process in processes if process.Name.lower() == process_name.lower()), None)
        if isinstance(pid, int):
            return pid
        else:
            return None
    except:
        return None
    

if __name__=='__main__':
    pid = get_yuanshen_pid()
    if pid:
        for i in range(5):
            psutil.Process(pid).resume()

    paused = False
    pause_time=0
    print('started')
    while True:
        try:
            # 获取当前前台应用名以及pid
            handle = win32gui.GetForegroundWindow()
            pid = win32process.GetWindowThreadProcessId(handle)[1]
            process_name = psutil.Process(pid).name()

            if process_name==name and paused:
                pid = get_yuanshen_pid()
                if pid:
                    psutil.Process(pid).resume()
                    paused = False
            elif process_name !=name and not paused:
                pid = get_yuanshen_pid()
                if pid:
                    psutil.Process(pid).suspend()
                    paused = True
        
            if paused:
                pause_time+=1
                if pause_time>=10:
                    pid = get_yuanshen_pid()
                    if pid:
                        psutil.Process(pid).resume()
                        time.sleep(resume_time)
                        psutil.Process(pid).suspend()
                    pause_time=0
            time.sleep(check_time)
        except BaseException as e:
            print(e)
            time.sleep(check_time)



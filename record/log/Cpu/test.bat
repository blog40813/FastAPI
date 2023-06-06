@echo off

REM 设置计数器初始值
set /a count=0

REM 设置持续时间为一天（以分钟为单位）
set /a duration=1440

REM 创建空白的日志文件
echo. > disk_usage.log
echo. > disk_usage_time.log

REM 开始循环，每分钟获取一次硬盘使用率和硬盘使用时间
:loop
REM 获取硬盘使用率
wmic logicaldisk get DeviceID, FreeSpace, Size, FileSystem, VolumeName >> disk_usage.log

REM 获取硬盘使用时间
smartctl.exe -a /dev/sda | findstr /C:"Power_On_Hours" >> disk_usage_time.log

REM 增加计数器
set /a count+=1

REM 判断是否达到持续时间
if %count% lss %duration% (
    REM 等待1分钟
    ping 127.0.0.1 -n 2 > nul
    goto loop
)

REM 输出完成消息
echo 获取硬盘使用率和使用时间已完成。

REM 暂停命令行窗口
pause
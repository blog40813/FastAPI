$duration = 1440  # 持续时间为一天（以分钟为单位）
$logFilePath = "disk_usage_time.log"  # 硬盘使用时间日志文件路径

# 创建空白的日志文件
echo. > disk_usage.log
echo. > disk_usage_time.log

# 获取硬盘使用时间并写入日志文件
while ($duration -gt 0) {
    $disk = Get-WmiObject -Class Win32_DiskDrive | Where-Object {$_.DeviceID -eq "PHYSICALDRIVE0"}
    $powerOnHours = $disk.PowerOnHours
    $powerOnMinutes = $powerOnHours * 60  # 使用时间以分钟为单位
    $powerOnTimeString = "Power_On_Hours: $powerOnHours, Power_On_Minutes: $powerOnMinutes"

    $powerOnTimeString | Out-File -FilePath $logFilePath -Append

    Start-Sleep -Seconds 60  # 等待1分钟
    $duration -= 1
}

Write-Host "获取硬盘使用时间已完成。"
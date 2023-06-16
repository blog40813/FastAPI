

$duration = 1440  # ?�续?�间为�?天�?以�??�为?��?�?
$logFilePath = "disk_usage_time.log"  # 硬�?使用?�间?��??�件路�?

# ?�建空白?�日志�?�?
New-Item -ItemType file -Path $logFilePath -Force | Out-Null

# ?��?硬�?使用?�间并�??�日志�?�?
while ($duration -gt 0) {
    $disk = Get-WmiObject -Class Win32_DiskDrive | Where-Object {$_.DeviceID -eq "PHYSICALDRIVE0"}
    $powerOnHours = $disk.PowerOnHours
    $powerOnMinutes = $powerOnHours * 60  # 使用?�间以�??�为?��?
    $powerOnTimeString = "Power_On_Hours: $powerOnHours, Power_On_Minutes: $powerOnMinutes"

    $powerOnTimeString | Out-File -FilePath $logFilePath -Append

    Start-Sleep -Seconds 60  # 等�?1?��?
    $duration -= 1
}

Write-Host yws


$duration = 1440  # ?ç»­?¶é—´ä¸ºä?å¤©ï?ä»¥å??Ÿä¸º?•ä?ï¼?
$logFilePath = "disk_usage_time.log"  # ç¡¬ç?ä½¿ç”¨?¶é—´?¥å??‡ä»¶è·¯å?

# ?›å»ºç©ºç™½?„æ—¥å¿—æ?ä»?
New-Item -ItemType file -Path $logFilePath -Force | Out-Null

# ?·å?ç¡¬ç?ä½¿ç”¨?¶é—´å¹¶å??¥æ—¥å¿—æ?ä»?
while ($duration -gt 0) {
    $disk = Get-WmiObject -Class Win32_DiskDrive | Where-Object {$_.DeviceID -eq "PHYSICALDRIVE0"}
    $powerOnHours = $disk.PowerOnHours
    $powerOnMinutes = $powerOnHours * 60  # ä½¿ç”¨?¶é—´ä»¥å??Ÿä¸º?•ä?
    $powerOnTimeString = "Power_On_Hours: $powerOnHours, Power_On_Minutes: $powerOnMinutes"

    $powerOnTimeString | Out-File -FilePath $logFilePath -Append

    Start-Sleep -Seconds 60  # ç­‰å?1?†é?
    $duration -= 1
}

Write-Host yws
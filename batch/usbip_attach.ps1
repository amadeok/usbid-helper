# USBIP Attach Script with Logging
$LogFile = "usbip_log.txt"
$ConfigFile = "usbip_conf.txt"

# Read configuration
try {
    $config = Get-Content $ConfigFile -ErrorAction Stop | ConvertFrom-StringData
    $server = $config.Server
    $busId = $config.BusId
}
catch {
    Write-Host "Error: Failed to read config file - $_" -ForegroundColor Red
    "Error: Failed to read config file - $_" | Out-File $LogFile -Append
    exit 1
}

# Validate configuration
if (-not $server) {
    Write-Host "Error: Server not specified in config file" -ForegroundColor Red
    "Error: Server not specified in config file" | Out-File $LogFile -Append
    exit 1
}

if (-not $busId) {
    Write-Host "Error: Bus ID not specified in config file" -ForegroundColor Red
    "Error: Bus ID not specified in config file" | Out-File $LogFile -Append
    exit 1
}

# Main connection loop
while ($true) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $message = "Attempting connection to $server for device $busId at $timestamp"
    
    Write-Host $message
    $message | Out-File $LogFile -Append

    try {
        $output = & "C:\Program Files\USBip\usbip.exe" attach -r $server -b $busId 2>&1
        
        # Log all output
        $output | Out-File $LogFile -Append
        
        if ($LASTEXITCODE -eq 0) {
            $successMessage = "Success at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
            Write-Host $successMessage -ForegroundColor Green
            $successMessage | Out-File $LogFile -Append
            exit 0
        }
        
        # If we get here, the command failed
        $errorMessage = "Attempt failed (Exit Code: $LASTEXITCODE), retrying in 1 second..."
        Write-Host $errorMessage -ForegroundColor Yellow
        $errorMessage | Out-File $LogFile -Append
    }
    catch {
        $errorMessage = "Error executing usbip: $_"
        Write-Host $errorMessage -ForegroundColor Red
        $errorMessage | Out-File $LogFile -Append
    }

    Start-Sleep -Seconds 1
}
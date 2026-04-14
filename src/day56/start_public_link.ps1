$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent (Split-Path -Parent $projectRoot)
$pythonPath = Join-Path $repoRoot ".venv\Scripts\python.exe"
$sshPath = "C:\Windows\System32\OpenSSH\ssh.exe"
$stdoutLog = Join-Path $projectRoot "localhostrun-stdout.log"
$stderrLog = Join-Path $projectRoot "localhostrun-stderr.log"
$appUrl = "http://127.0.0.1:5000/health"

if (-not (Test-Path $pythonPath)) {
    throw "Python executable not found at $pythonPath"
}

try {
    Invoke-RestMethod -Uri $appUrl -TimeoutSec 3 | Out-Null
    Write-Host "Flask app is already running on port 5000."
} catch {
    $appProcess = Start-Process -FilePath $pythonPath -ArgumentList "app.py" -WorkingDirectory $projectRoot -PassThru
    Write-Host "Started Flask app. PID: $($appProcess.Id)"
    Start-Sleep -Seconds 4
}

Remove-Item -LiteralPath $stdoutLog, $stderrLog -ErrorAction SilentlyContinue

$sshProcess = Start-Process `
    -FilePath $sshPath `
    -ArgumentList "-o", "StrictHostKeyChecking=no", "-o", "ExitOnForwardFailure=yes", "-R", "80:localhost:5000", "nokey@localhost.run" `
    -RedirectStandardOutput $stdoutLog `
    -RedirectStandardError $stderrLog `
    -PassThru

Write-Host "Started localhost.run tunnel. PID: $($sshProcess.Id)"
Start-Sleep -Seconds 8

if (-not (Test-Path $stdoutLog)) {
    throw "Tunnel log was not created."
}

$match = Select-String -Path $stdoutLog -Pattern "https://[a-zA-Z0-9.-]+" | Select-Object -First 1
if ($match) {
    Write-Host ""
    Write-Host "Public URL:"
    Write-Host $match.Matches[0].Value
} else {
    Write-Host ""
    Write-Host "Tunnel did not return a public URL yet. Check these logs:"
    Write-Host $stdoutLog
    Write-Host $stderrLog
}

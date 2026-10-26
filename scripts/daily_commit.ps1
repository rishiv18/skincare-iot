# Daily auto-commit: adds today's progress entry to README.md, then commits
# and pushes it with any changes to tracked files (e.g. new sensor readings).
# New files must be added manually.

$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo
$log = Join-Path $PSScriptRoot "daily_commit.log"

function Write-Log($msg) {
    "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $msg" | Out-File -FilePath $log -Append -Encoding utf8
}

python "$PSScriptRoot\update_progress.py"
if ($LASTEXITCODE -ne 0) { Write-Log "README update FAILED (exit $LASTEXITCODE)." }

git add -u
git add README.md
$changed = git diff --cached --name-only
if (-not $changed) {
    Write-Log "No changes - nothing committed."
    exit 0
}

$date = Get-Date -Format 'yyyy-MM-dd'
$files = ($changed -join ', ')
git commit -m "Daily update $date" -m "Changed: $files" | Out-Null
git push origin main 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) { Write-Log "Committed and pushed: $files" }
else { Write-Log "Commit made but push FAILED (exit $LASTEXITCODE)." }

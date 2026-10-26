# Daily auto-commit: commits and pushes changes to tracked files (e.g. new
# sensor readings in skincare_data.db / skincare_dataset.csv).
# Skips the commit when nothing has changed. New files must be added manually.

$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo
$log = Join-Path $PSScriptRoot "daily_commit.log"

function Write-Log($msg) {
    "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $msg" | Out-File -FilePath $log -Append -Encoding utf8
}

git add -u
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

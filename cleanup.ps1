# PowerShell script to keep only essential files for the Easy OpenCV library

# Define the essential files and directories to keep
$EssentialFiles = @(
    "README.md",
    "requirements.txt",
    "setup.py",
    "pyproject.toml", 
    "LICENSE",
    "MANIFEST.in",
    "easy_opencv"
)

Write-Host "`n===== Essential Files Cleanup ====="
Write-Host "This will keep ONLY essential files and remove everything else.`n"

# Ask for confirmation
$confirmation = Read-Host "This is a DESTRUCTIVE operation. Are you sure? (type 'YES' to confirm)"
if ($confirmation -ne "YES") {
    Write-Host "Cleanup cancelled."
    exit
}

$removedCount = 0
$removedItems = @()

# Process all items in the directory
Get-ChildItem -Path $PSScriptRoot -Force | ForEach-Object {
    $itemName = $_.Name
    
    # Skip the script itself
    if ($itemName -eq "cleanup.ps1") {
        Write-Host "Keeping script: $itemName"
        return
    }
    
    # Skip essential files
    if ($EssentialFiles -contains $itemName) {
        Write-Host "Keeping essential: $itemName"
        return
    }
    
    # Skip .git directory
    if ($itemName -eq ".git") {
        Write-Host "Keeping Git repository: $itemName"
        return
    }
    
    # Remove everything else
    if ($_.PSIsContainer) {
        # It's a directory
        Remove-Item -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "Removed directory: $itemName"
    } else {
        # It's a file
        Remove-Item -Path $_.FullName -Force -ErrorAction SilentlyContinue
        Write-Host "Removed file: $itemName"
    }
    
    $removedItems += $itemName
    $removedCount++
}

# Generate report
$reportContent = "# Essential Files Cleanup Report`n`n"
$reportContent += "Cleanup performed on: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n`n"
$reportContent += "## $removedCount items removed`n`n"

foreach ($item in ($removedItems | Sort-Object)) {
    $reportContent += "- ``$item```n"
}

$reportContent += "`n`n## Kept Essential Files`n`n"

foreach ($item in ($EssentialFiles | Sort-Object)) {
    $reportContent += "- ``$item```n"
}

Set-Content -Path "$PSScriptRoot\CLEANUP_REPORT.md" -Value $reportContent

Write-Host "`nRemoved $removedCount non-essential items."
Write-Host "The library now contains only core essential files needed for distribution."
Write-Host "Cleanup report written to CLEANUP_REPORT.md"

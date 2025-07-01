# PowerShell script to keep only essential files for the Easy OpenCV library

# Define the essential files and directories to keep
$EssentialFiles = @(
    "README.md",
    "requirements.txt",
    "setup.py",
    "pyproject.toml", 
    "LICENSE",
    "MANIFEST.in",
    "easy_opencv"  # Core library directory
)

# Define the current directory
$RootDir = $PSScriptRoot

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
Get-ChildItem -Path $RootDir -Force | ForEach-Object {
    $itemName = $_.Name
    $itemPath = $_.FullName
    
    # Skip the script itself
    if ($itemName -eq "keep_essential_files.ps1") {
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
    try {
        if ($_.PSIsContainer) {
            # It's a directory
            Remove-Item -Path $itemPath -Recurse -Force
            Write-Host "Removed directory: $itemName"
        } else {
            # It's a file
            Remove-Item -Path $itemPath -Force
            Write-Host "Removed file: $itemName"
        }
        
        $removedItems += $itemName
        $removedCount++
    }
    catch {
        Write-Host "Error removing $itemName: $($_.Exception.Message)"
    }
}

# Generate report
$reportContent = @"
# Essential Files Cleanup Report

Cleanup performed on: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## $removedCount items removed

$(($removedItems | Sort-Object | ForEach-Object { "- ``$_``" }) -join "`n")

## Kept Essential Files

$(($EssentialFiles | Sort-Object | ForEach-Object { "- ``$_``" }) -join "`n")
"@

Set-Content -Path "$RootDir\CLEANUP_REPORT.md" -Value $reportContent

Write-Host "`nRemoved $removedCount non-essential items."
Write-Host "The library now contains only core essential files needed for distribution."
Write-Host "Cleanup report written to CLEANUP_REPORT.md"

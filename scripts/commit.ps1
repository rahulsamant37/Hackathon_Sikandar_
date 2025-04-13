# PowerShell script to help create conventional commits

# Colors
$RED = [System.ConsoleColor]::Red
$GREEN = [System.ConsoleColor]::Green
$YELLOW = [System.ConsoleColor]::Yellow
$BLUE = [System.ConsoleColor]::Blue

# Commit types
$TYPES = @("feat", "fix", "docs", "style", "refactor", "perf", "test", "chore", "ci")
$TYPES_DESC = @(
    "A new feature",
    "A bug fix",
    "Documentation only changes",
    "Changes that do not affect the meaning of the code",
    "A code change that neither fixes a bug nor adds a feature",
    "A code change that improves performance",
    "Adding missing tests or correcting existing tests",
    "Changes to the build process or auxiliary tools",
    "Changes to CI configuration files and scripts"
)

# Common scopes
$SCOPES = @("backend", "frontend", "api", "auth", "courses", "modules", "content", "analytics", "ai", "infra", "db", "ui", "docs", "tests", "deps", "config")

# Print header
Write-Host "=== Conventional Commit Helper ===" -ForegroundColor $BLUE
Write-Host "This script helps you create a commit message following the Conventional Commits specification."
Write-Host "Learn more: https://www.conventionalcommits.org/"
Write-Host ""

# Select commit type
Write-Host "Select commit type:" -ForegroundColor $YELLOW
for ($i = 0; $i -lt $TYPES.Length; $i++) {
    Write-Host "$i: " -NoNewline
    Write-Host $TYPES[$i] -ForegroundColor $GREEN -NoNewline
    Write-Host " - $($TYPES_DESC[$i])"
}

$type_num = Read-Host "Enter type number"
if (-not ($type_num -match "^\d+$") -or [int]$type_num -ge $TYPES.Length) {
    Write-Host "Invalid selection. Exiting." -ForegroundColor $RED
    exit 1
}

$TYPE = $TYPES[[int]$type_num]

# Select scope
Write-Host "`nSelect scope (or enter custom scope):" -ForegroundColor $YELLOW
for ($i = 0; $i -lt $SCOPES.Length; $i++) {
    Write-Host "$i: " -NoNewline
    Write-Host $SCOPES[$i] -ForegroundColor $GREEN
}
Write-Host "c: " -NoNewline
Write-Host "custom scope" -ForegroundColor $GREEN
Write-Host "n: " -NoNewline
Write-Host "no scope" -ForegroundColor $GREEN

$scope_option = Read-Host "Enter scope option"

if ($scope_option -eq "c") {
    $SCOPE = Read-Host "Enter custom scope"
}
elseif ($scope_option -eq "n") {
    $SCOPE = ""
}
elseif ($scope_option -match "^\d+$" -and [int]$scope_option -lt $SCOPES.Length) {
    $SCOPE = $SCOPES[[int]$scope_option]
}
else {
    Write-Host "Invalid selection. Exiting." -ForegroundColor $RED
    exit 1
}

# Enter subject
Write-Host "`nEnter commit subject (short description):" -ForegroundColor $YELLOW
$SUBJECT = Read-Host "> "

if ([string]::IsNullOrEmpty($SUBJECT)) {
    Write-Host "Subject cannot be empty. Exiting." -ForegroundColor $RED
    exit 1
}

# Enter body (optional)
Write-Host "`nEnter commit body (optional, press Enter to skip):" -ForegroundColor $YELLOW
$BODY = Read-Host "> "

# Enter footer (optional)
Write-Host "`nEnter commit footer (optional, press Enter to skip):" -ForegroundColor $YELLOW
Write-Host "Example: 'Closes #123' or 'BREAKING CHANGE: <description>'"
$FOOTER = Read-Host "> "

# Build commit message
if ([string]::IsNullOrEmpty($SCOPE)) {
    $COMMIT_MSG = "$TYPE`: $SUBJECT"
}
else {
    $COMMIT_MSG = "$TYPE($SCOPE): $SUBJECT"
}

if (-not [string]::IsNullOrEmpty($BODY)) {
    $COMMIT_MSG = "$COMMIT_MSG`n`n$BODY"
}

if (-not [string]::IsNullOrEmpty($FOOTER)) {
    $COMMIT_MSG = "$COMMIT_MSG`n`n$FOOTER"
}

# Preview commit message
Write-Host "`n=== Commit Message Preview ===" -ForegroundColor $BLUE
Write-Host $COMMIT_MSG
Write-Host "=============================" -ForegroundColor $BLUE

# Confirm and commit
Write-Host "`nDo you want to commit with this message? (y/n)" -ForegroundColor $YELLOW
$CONFIRM = Read-Host "> "

if ($CONFIRM -eq "y" -or $CONFIRM -eq "Y") {
    $COMMIT_MSG | git commit -F -
    Write-Host "Commit created successfully!" -ForegroundColor $GREEN
}
else {
    Write-Host "Commit cancelled." -ForegroundColor $RED
    exit 0
}

<#
.SYNOPSIS
    One entry point for the "Manim for STEM teachers" workshop.

.DESCRIPTION
    Commands
      setup     Create (or update) the conda environment "manim-workshop"
      check     Show the versions of conda, Manim, FFmpeg, LaTeX and git
      preview   Render one scene quickly and open it        -Scene 01  [-Quality l]
      render    Render scenes and copy them into docs/       [-Only 05] [-Quality m]
      serve     Start the website locally and open it        [-Port 8000]
      slides    Same as serve, but opens the slide deck      [-Port 8000]
      all       render + serve
      seturl    Point the website's GitHub links to your repo -RepoUrl https://github.com/<you>/<repo>
      publish   seturl + git init/commit/push to GitHub      -RepoUrl https://github.com/<you>/<repo>
      help      Show this help

.EXAMPLE
    .\run.ps1 setup
    .\run.ps1 preview -Scene 05
    .\run.ps1 render -Quality h
    .\run.ps1 serve
    .\run.ps1 publish -RepoUrl https://github.com/YouvenZ/manim-stem-workshop

.NOTES
    If Windows refuses to run scripts, start it with:
        powershell -ExecutionPolicy Bypass -File .\run.ps1 serve
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet("setup", "check", "preview", "render", "serve", "slides", "all", "seturl", "publish", "help")]
    [string]$Command = "help",

    [string]$Scene = "00",
    [string]$Only = "",
    [ValidateSet("l", "m", "h", "k")]
    [string]$Quality = "",
    [int]$Port = 8000,
    [string]$RepoUrl = "",
    [string]$Message = "Update Manim workshop"
)

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
$EnvName = "manim-workshop"
Set-Location $Root

function Write-Step([string]$text) { Write-Host "`n==> $text" -ForegroundColor Cyan }

function Assert-Conda {
    if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
        throw "conda was not found. Install Anaconda/Miniconda, or open an 'Anaconda PowerShell Prompt'."
    }
}

function Test-EnvExists {
    $envs = conda env list | Out-String
    return ($envs -match "(?m)^$EnvName\s")
}

# Run a program inside the conda env without having to 'conda activate'.
function Invoke-InEnv([string[]]$Arguments) {
    Assert-Conda
    if (-not (Test-EnvExists)) { throw "Environment '$EnvName' not found. Run:  .\run.ps1 setup" }
    & conda run --no-capture-output -n $EnvName @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Command failed (exit $LASTEXITCODE): $($Arguments -join ' ')" }
}

function Invoke-Git([string[]]$Arguments) {
    & git @Arguments
    if ($LASTEXITCODE -ne 0) { throw "git $($Arguments -join ' ') failed (exit $LASTEXITCODE)" }
}

function Get-SceneFile([string]$prefix) {
    $file = Get-ChildItem (Join-Path $Root "scenes") -Filter "$prefix*.py" | Select-Object -First 1
    if (-not $file) { throw "No scene in scenes/ starts with '$prefix'." }
    return $file
}

function Get-SceneClass($file) {
    $match = Select-String -Path $file.FullName -Pattern "^class\s+(\w+)\s*\(" | Select-Object -First 1
    if (-not $match) { throw "No Scene class found in $($file.Name)." }
    return $match.Matches[0].Groups[1].Value
}

function Start-Site([string]$path) {
    $url = "http://localhost:$Port/$path"
    Write-Step "Serving docs/ at $url   (press Ctrl+C to stop)"
    # open the browser shortly after the server starts
    Start-Job -ScriptBlock { Start-Sleep -Seconds 2; Start-Process $using:url } | Out-Null
    Invoke-InEnv @("python", "-m", "http.server", "$Port", "--directory", (Join-Path $Root "docs"))
}

function Set-RepoUrl([string]$url) {
    if (-not $url) { throw "Give your repository URL, e.g.  -RepoUrl https://github.com/<you>/manim-stem-workshop" }
    $url = $url.Trim().TrimEnd("/") -replace "\.git$", ""
    if ($url -notmatch "^https://github\.com/[^/]+/[^/]+$") {
        throw "RepoUrl must look like https://github.com/<user>/<repo>  (got: $url)"
    }
    $utf8 = New-Object System.Text.UTF8Encoding($false)
    $edits = @(
        @{ File = "docs\assets\js\examples.js"; Pattern = 'window\.REPO_URL = "[^"]*";'; Value = "window.REPO_URL = `"$url`";" },
        @{ File = "docs\index.html";            Pattern = 'https://github\.com/[^/<\s]+/[^/<\s.]+(?=</span>\.git)'; Value = $url },
        @{ File = "docs\slides\index.html";     Pattern = 'git clone https://github\.com/[^\s<]+\.git'; Value = "git clone $url.git" }
    )
    foreach ($e in $edits) {
        $path = Join-Path $Root $e.File
        $text = [System.IO.File]::ReadAllText($path, $utf8)
        $new = [regex]::Replace($text, $e.Pattern, $e.Value)
        if ($new -ne $text) { [System.IO.File]::WriteAllText($path, $new, $utf8); Write-Host "  updated $($e.File)" }
        else { Write-Host "  $($e.File) already up to date" }
    }
    return $url
}

switch ($Command) {

    "setup" {
        Assert-Conda
        if (Test-EnvExists) {
            Write-Step "Updating conda environment '$EnvName'"
            conda env update -n $EnvName -f environment.yml --prune
        } else {
            Write-Step "Creating conda environment '$EnvName' (a few minutes the first time)"
            conda env create -f environment.yml
        }
        if ($LASTEXITCODE -ne 0) { throw "conda failed." }
        Invoke-InEnv @("manim", "--version")
        if (-not (Get-Command latex -ErrorAction SilentlyContinue)) {
            Write-Warning "LaTeX not found: install MiKTeX (https://miktex.org/download) for MathTex scenes."
        }
        Write-Host "`nReady. Try:  .\run.ps1 preview -Scene 00" -ForegroundColor Green
    }

    "check" {
        Assert-Conda
        Write-Step "Versions"
        conda --version
        Invoke-InEnv @("manim", "--version")
        Invoke-InEnv @("ffmpeg", "-hide_banner", "-version") | Select-Object -First 1
        if (Get-Command latex -ErrorAction SilentlyContinue) { (latex --version | Select-Object -First 1) } else { Write-Warning "LaTeX: not found" }
        if (Get-Command git -ErrorAction SilentlyContinue) { git --version } else { Write-Warning "git: not found" }
    }

    "preview" {
        $file = Get-SceneFile $Scene
        $cls = Get-SceneClass $file
        $q = if ($Quality) { $Quality } else { "l" }
        Write-Step "Rendering $($file.Name) -> $cls at quality '$q'"
        Invoke-InEnv @("manim", "-p", "-q$q", "--media_dir", "build/media", "scenes/$($file.Name)", $cls)
    }

    "render" {
        $q = if ($Quality) { $Quality } else { "m" }
        Write-Step "Rendering scenes (quality '$q') into docs/"
        $renderArgs = @("python", "scripts/render_all.py", "-q", $q)
        if ($Only) { $renderArgs += @("--only", $Only) }
        Invoke-InEnv $renderArgs
    }

    "serve"  { Start-Site "" }
    "slides" { Start-Site "slides/" }

    "all" {
        $q = if ($Quality) { $Quality } else { "m" }
        Invoke-InEnv @("python", "scripts/render_all.py", "-q", $q)
        Start-Site ""
    }

    "seturl" {
        Write-Step "Pointing the website links to your repository"
        $url = Set-RepoUrl $RepoUrl
        Write-Host "Done: $url" -ForegroundColor Green
    }

    "publish" {
        if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "git is not installed." }
        $videos = @(Get-ChildItem (Join-Path $Root "docs\videos") -Filter *.mp4 -ErrorAction SilentlyContinue)
        if ($videos.Count -eq 0) { throw "docs/videos is empty. Run  .\run.ps1 render  first." }

        Write-Step "1/4  Repository links"
        $url = Set-RepoUrl $RepoUrl

        Write-Step "2/4  Local git repository"
        # Check for .git HERE: a parent folder may itself be a git repo.
        if (-not (Test-Path (Join-Path $Root ".git"))) {
            Invoke-Git @("init")
            Write-Host "  initialised a new repository in $Root"
        }
        Invoke-Git @("branch", "-M", "main")
        $remotes = @(git remote)
        if ($remotes -contains "origin") { Invoke-Git @("remote", "set-url", "origin", "$url.git") }
        else { Invoke-Git @("remote", "add", "origin", "$url.git") }
        Write-Host "  origin -> $url.git"

        Write-Step "3/4  Commit"
        Invoke-Git @("add", "-A")
        $pending = git status --porcelain
        if ($pending) { Invoke-Git @("commit", "-m", $Message) } else { Write-Host "  nothing new to commit" }

        Write-Step "4/4  Push to GitHub (a browser sign-in window may appear the first time)"
        Invoke-Git @("push", "-u", "origin", "main")

        $parts = $url -split "/"
        $owner = $parts[3].ToLower(); $repo = $parts[4]
        Write-Host ""
        Write-Host "Pushed. Remaining one-time step on GitHub:" -ForegroundColor Green
        Write-Host "  $url/settings/pages  ->  Build and deployment -> Source: GitHub Actions"
        Write-Host "Then watch the deployment:  $url/actions"
        Write-Host "Website:  https://$owner.github.io/$repo/"
        Write-Host "Slides:   https://$owner.github.io/$repo/slides/"
    }

    default { Get-Help $PSCommandPath -Detailed }
}

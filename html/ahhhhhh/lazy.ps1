function Ask-Yes($question) {
    while ($true) {
        $answer = Read-Host "$question [Y/n]"

        if ($answer -eq '' -or $answer -eq 'y' -or $answer -eq 'yes') {
            return $true
        }

        if ($answer -eq 'n' -or $answer -eq 'no') {
            return $false
        }

        Write-Host 'Please type Y or N.'
    }
}

function Choose-Option($title, $options) {
    Write-Host ''
    Write-Host $title -ForegroundColor Cyan
    Write-Host 'Use the arrow keys and Enter. Press Esc to cancel.'

    try {
        if ([Console]::IsInputRedirected -or [Console]::IsOutputRedirected) {
            throw 'No interactive console'
        }

        $selected = 0
        $normalColor = [Console]::ForegroundColor

        for ($i = 0; $i -lt $options.Count; $i++) {
            [Console]::WriteLine()
        }

        $top = [Console]::CursorTop - $options.Count
        $width = [Console]::WindowWidth - 1

        if ($top -lt 0 -or $width -lt 5) {
            throw 'Terminal is too small'
        }

        while ($true) {
            for ($i = 0; $i -lt $options.Count; $i++) {
                [Console]::SetCursorPosition(0, $top + $i)

                if ($i -eq $selected) {
                    $line = '> ' + $options[$i]
                    [Console]::ForegroundColor = [ConsoleColor]::Green
                }
                else {
                    $line = '  ' + $options[$i]
                    [Console]::ForegroundColor = $normalColor
                }

                if ($line.Length -gt $width) {
                    $line = $line.Substring(0, $width)
                }

                [Console]::Write($line.PadRight($width))
            }

            [Console]::ForegroundColor = $normalColor
            [Console]::SetCursorPosition(0, $top + $options.Count)
            $key = [Console]::ReadKey($true).Key

            if ($key -eq [ConsoleKey]::UpArrow) {
                $selected--
                if ($selected -lt 0) {
                    $selected = $options.Count - 1
                }
            }

            if ($key -eq [ConsoleKey]::DownArrow) {
                $selected++
                if ($selected -ge $options.Count) {
                    $selected = 0
                }
            }

            if ($key -eq [ConsoleKey]::Enter) {
                Write-Host ''
                return $selected
            }

            if ($key -eq [ConsoleKey]::Escape) {
                Write-Host ''
                return -1
            }
        }
    }
    catch {
        for ($i = 0; $i -lt $options.Count; $i++) {
            Write-Host "$($i + 1)) $($options[$i])"
        }

        while ($true) {
            $answer = Read-Host 'Enter a number (or Q to cancel)'

            if ($answer -eq 'q') {
                return -1
            }

            $number = 0
            if ([int]::TryParse($answer, [ref]$number)) {
                if ($number -ge 1 -and $number -le $options.Count) {
                    return $number - 1
                }
            }
        }
    }
    finally {
        if ($null -ne $normalColor) {
            [Console]::ForegroundColor = $normalColor
        }
    }
}

$projectTypes = @('FastAPI', 'FastAPI + HTML', 'Flask', 'Custom', 'Exit')
$type = Choose-Option 'What kind of project do you want?' $projectTypes

if ($type -eq -1 -or $type -eq 4) {
    return
}

$isFastAPI = $type -eq 0 -or $type -eq 1
$isFlask = $type -eq 2
$isFramework = $isFastAPI -or $isFlask
$isHtml = $type -eq 1 -or $isFlask

$projectName = (Read-Host 'Project name').Trim()

if ($projectName -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]*$' -or $projectName.EndsWith('.')) {
    Write-Host 'Invalid project name. Use letters, numbers, dots, dashes or underscores.' -ForegroundColor Red
    return
}

$folders = @('This folder', 'New subfolder', 'Cancel')
$place = Choose-Option 'Where should the project go?' $folders

if ($place -eq -1 -or $place -eq 2) {
    return
}

$existingProject = $false
if ($place -eq 0 -and (Test-Path 'pyproject.toml')) {
    $existingProject = $true
}

$packageName = $projectName.ToLower().Replace('-', '_').Replace('.', '_')

if ($existingProject) {
    $usePackage = $false

    if (Test-Path 'src') {
        foreach ($folder in (Get-ChildItem 'src' -Directory)) {
            if (Test-Path (Join-Path $folder.FullName '__init__.py')) {
                $usePackage = $true
            }
        }
    }

    Write-Host 'An existing project was found. Keeping its current layout.' -ForegroundColor Yellow
}
else {
    $layouts = @("Package (src/$packageName)", 'No package (src/main.py)', 'Cancel')
    $layout = Choose-Option 'Which project layout do you want?' $layouts

    if ($layout -eq -1 -or $layout -eq 2) {
        return
    }

    $usePackage = $layout -eq 0
}

$runType = -1

if ($isFastAPI) {
    $choices = @('FastAPI CLI (fastapi dev)', 'Uvicorn CLI (uvicorn --reload)', 'Python directly (python main.py)')
    $runType = Choose-Option 'How do you want to run FastAPI?' $choices
}
elseif ($isFlask) {
    $choices = @('Flask CLI (flask run --debug)', 'Python directly (python main.py)')
    $runType = Choose-Option 'How do you want to run Flask?' $choices
}

if ($isFramework -and $runType -eq -1) {
    return
}

$projectFolder = (Get-Location).Path

if ($place -eq 1) {
    $firstName = ($projectName -split '\.')[0].ToUpper()
    $reserved = @('CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9')

    if ($reserved -contains $firstName) {
        Write-Host 'That is a reserved Windows folder name.' -ForegroundColor Red
        return
    }

    $projectFolder = Join-Path $projectFolder $projectName

    if (Test-Path -LiteralPath $projectFolder) {
        Write-Host 'That folder already exists.' -ForegroundColor Yellow
        return
    }
}

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    if (-not (Ask-Yes 'uv is not installed. Install it?')) {
        return
    }

    Write-Host 'Installing uv...'
    powershell.exe -NoProfile -ExecutionPolicy Bypass -Command 'irm https://astral.sh/uv/install.ps1 | iex'

    if ($LASTEXITCODE -ne 0) {
        Write-Host 'Could not install uv.' -ForegroundColor Red
        return
    }

    $uvFolder = Join-Path $HOME '.local\bin'
    if (Test-Path (Join-Path $uvFolder 'uv.exe')) {
        $env:Path = "$uvFolder;$env:Path"
    }

    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        Write-Host 'uv is installed, but it is not in PATH yet. Restart the terminal.' -ForegroundColor Yellow
        return
    }
}

Write-Host "Selected: $($projectTypes[$type])"

if ($place -eq 1) {
    if ($usePackage) {
        uv init --package $projectName
    }
    else {
        uv init --no-package $projectName
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Host 'Could not create the project.' -ForegroundColor Red
        return
    }

    Set-Location -LiteralPath $projectFolder
}
elseif ($existingProject) {
    Write-Host 'Using the existing uv project.'
}
else {
    if ($usePackage) {
        uv init --package --name $projectName
    }
    else {
        uv init --no-package --name $projectName
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Host 'Could not create the project.' -ForegroundColor Red
        return
    }
}

$ignoreFile = Join-Path (Get-Location).Path '.gitignore'
$ignoreRules = @(
    '__pycache__/'
    '*.py[oc]'
    'build/'
    'dist/'
    'wheels/'
    '*.egg-info'
    '.venv'
    '.pytest_cache/'
    '.mypy_cache/'
    '.ruff_cache/'
    '.coverage'
    'htmlcov/'
    '.env'
    '.env.*'
    '!.env.example'
    '.idea/'
    '.DS_Store'
    'Thumbs.db'
)

if (-not (Test-Path -LiteralPath $ignoreFile)) {
    Set-Content -LiteralPath $ignoreFile -Value $ignoreRules -Encoding UTF8
    Write-Host 'Created .gitignore.' -ForegroundColor Green
}
else {
    $currentRules = @(Get-Content -LiteralPath $ignoreFile)
    $missingRules = @()

    foreach ($rule in $ignoreRules) {
        if ($currentRules -notcontains $rule) {
            $missingRules += $rule
        }
    }

    if ($missingRules.Count -gt 0) {
        Add-Content -LiteralPath $ignoreFile -Value '' -Encoding UTF8
        Add-Content -LiteralPath $ignoreFile -Value $missingRules -Encoding UTF8
        Write-Host 'Updated .gitignore.' -ForegroundColor Green
    }
    else {
        Write-Host '.gitignore is already up to date.'
    }
}

$moduleName = $packageName
$moduleFolder = 'src'

if ($usePackage) {
    $moduleFolder = Join-Path 'src' $packageName

    if (-not (Test-Path (Join-Path $moduleFolder '__init__.py'))) {
        $packages = @()

        if (Test-Path 'src') {
            foreach ($folder in (Get-ChildItem 'src' -Directory)) {
                if (Test-Path (Join-Path $folder.FullName '__init__.py')) {
                    $packages += $folder
                }
            }
        }

        if ($packages.Count -eq 1) {
            $moduleFolder = $packages[0].FullName
            $moduleName = $packages[0].Name
        }
        else {
            Write-Host 'Could not find the package folder created by uv init.' -ForegroundColor Red
            return
        }
    }
}

$mainFile = Join-Path $moduleFolder 'main.py'
$mainDisplay = 'src/main.py'
$appImport = 'main:app'
$pythonImport = 'src.main:app'

if ($usePackage) {
    $mainDisplay = "src/$moduleName/main.py"
    $appImport = "${moduleName}.main:app"
    $pythonImport = $appImport
}

if ($isFramework -and (Test-Path -LiteralPath $mainFile)) {
    Write-Host "$mainDisplay already exists. Keeping it." -ForegroundColor Yellow
}

if ($type -eq 3) {
    if (Test-Path -LiteralPath $mainFile) {
        Write-Host "$mainDisplay already exists. Keeping it." -ForegroundColor Yellow
    }
    elseif ($usePackage) {
        $initFile = Join-Path $moduleFolder '__init__.py'

        if ($existingProject) {
            $customCode = @"
def main():
    print("Hello from $projectName!")

if __name__ == "__main__":
    main()
"@
            Set-Content -LiteralPath $mainFile -Value $customCode -Encoding UTF8
            Write-Host 'Created main.py. Existing project entry points were left unchanged.' -ForegroundColor Green
        }
        else {
            $customCode = Get-Content -LiteralPath $initFile -Raw
            if ($customCode -notmatch 'def main\(') {
                Write-Host 'uv did not generate its usual main function.' -ForegroundColor Yellow
                $customCode = @"
def main():
    print("Hello from $projectName!")
"@
            }

            $customCode += @'

if __name__ == "__main__":
    main()
'@
            Set-Content -LiteralPath $mainFile -Value $customCode -Encoding UTF8
            Set-Content -LiteralPath $initFile -Value 'from .main import main' -Encoding UTF8
            Write-Host 'Created main.py and linked the uv project command to it.' -ForegroundColor Green
        }
    }
    else {
        if (-not (Test-Path 'src')) {
            New-Item -ItemType Directory -Path 'src' | Out-Null
        }

        if (-not $existingProject -and (Test-Path 'main.py')) {
            Move-Item -LiteralPath 'main.py' -Destination $mainFile
        }
        else {
            $customCode = @"
def main():
    print("Hello from $projectName!")

if __name__ == "__main__":
    main()
"@
            Set-Content -LiteralPath $mainFile -Value $customCode -Encoding UTF8
        }

        Write-Host 'Created src/main.py.' -ForegroundColor Green
    }
}

if (-not $isFramework) {
    if (-not (Ask-Yes 'Create or use a virtual environment here?')) {
        return
    }
}

$venv = Join-Path (Get-Location).Path '.venv'
$scriptsFolder = Join-Path $venv 'Scripts'

if (-not (Test-Path -LiteralPath (Join-Path $venv 'pyvenv.cfg'))) {
    if (Test-Path -LiteralPath $venv) {
        Write-Host '.venv exists but does not look valid.' -ForegroundColor Red
        return
    }

    Write-Host 'Creating .venv...'
    uv venv

    if ($LASTEXITCODE -ne 0) {
        Write-Host 'Could not create .venv.' -ForegroundColor Red
        return
    }
}
else {
    Write-Host 'Using existing .venv.'
}

if ($isFastAPI) {
    Write-Host 'Installing FastAPI...'

    if ($runType -eq 0) {
        if ($isHtml) {
            uv add 'fastapi[standard]' jinja2
        }
        else {
            uv add 'fastapi[standard]'
        }
    }
    else {
        if ($isHtml) {
            uv add fastapi 'uvicorn[standard]' jinja2
        }
        else {
            uv add fastapi 'uvicorn[standard]'
        }
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Host 'Could not install FastAPI.' -ForegroundColor Red
        return
    }
}
elseif ($isFlask) {
    Write-Host 'Installing Flask...'
    uv add flask

    if ($LASTEXITCODE -ne 0) {
        Write-Host 'Could not install Flask.' -ForegroundColor Red
        return
    }
}

if ($isFramework) {
    if ($type -eq 1) {
        $pythonCode = @"
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

folder = Path(__file__).resolve().parent

app = FastAPI()
app.mount("/static", StaticFiles(directory=str(folder / "static")), name="static")
templates = Jinja2Templates(directory=str(folder / "templates"))

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"project_name": "$projectName"})
"@

        if ($runType -eq 2) {
            $pythonCode = $pythonCode.Replace('from pathlib import Path', "from pathlib import Path`r`nimport uvicorn")
            $pythonCode += @"

if __name__ == "__main__":
    uvicorn.run("$pythonImport", reload=True)
"@
        }
    }
    elseif ($isFlask) {
        $pythonCode = @"
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html", project_name="$projectName")
"@

        if ($runType -eq 1) {
            $pythonCode += @'

if __name__ == "__main__":
    app.run(debug=True)
'@
        }
    }
    else {
        $pythonCode = @'
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello"}
'@

        if ($runType -eq 2) {
            $pythonCode = "import uvicorn`r`n" + $pythonCode
            $pythonCode += @"

if __name__ == "__main__":
    uvicorn.run("$pythonImport", reload=True)
"@
        }
    }

    if ($isHtml) {
        $templateFolder = Join-Path $moduleFolder 'templates'
        $staticFolder = Join-Path $moduleFolder 'static'
        $folderDisplay = $moduleFolder.Replace('\', '/')

        if (-not (Test-Path -LiteralPath $templateFolder)) {
            New-Item -ItemType Directory -Path $templateFolder | Out-Null
        }

        if (-not (Test-Path -LiteralPath $staticFolder)) {
            New-Item -ItemType Directory -Path $staticFolder | Out-Null
        }

        $cssLink = "{{ url_for('static', path='/style.css') }}"
        if ($isFlask) {
            $cssLink = "{{ url_for('static', filename='style.css') }}"
        }

        $htmlFile = Join-Path $templateFolder 'index.html'
        if (-not (Test-Path -LiteralPath $htmlFile)) {
            $htmlCode = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ project_name }}</title>
    <link rel="stylesheet" href="$cssLink">
</head>
<body>
    <h1>{{ project_name }}</h1>
</body>
</html>
"@
            Set-Content -LiteralPath $htmlFile -Value $htmlCode -Encoding UTF8
            Write-Host "Created $folderDisplay/templates/index.html." -ForegroundColor Green
        }

        $cssFile = Join-Path $staticFolder 'style.css'
        if (-not (Test-Path -LiteralPath $cssFile)) {
            $cssCode = @'
body {
    font-family: Arial, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    margin: 0;
}
'@
            Set-Content -LiteralPath $cssFile -Value $cssCode -Encoding UTF8
            Write-Host "Created $folderDisplay/static/style.css." -ForegroundColor Green
        }
    }

    if (-not (Test-Path -LiteralPath $mainFile)) {
        if (-not (Test-Path -LiteralPath $moduleFolder)) {
            New-Item -ItemType Directory -Path $moduleFolder | Out-Null
        }

        Set-Content -LiteralPath $mainFile -Value $pythonCode -Encoding UTF8

        if (-not $usePackage -and -not $existingProject -and (Test-Path -LiteralPath 'main.py')) {
            Remove-Item -LiteralPath 'main.py'
        }

        Write-Host "Created $mainDisplay." -ForegroundColor Green
    }
}

if ($isFramework) {
    $config = @{
        name = 'App'
        type = 'debugpy'
        request = 'launch'
        console = 'integratedTerminal'
        cwd = '${workspaceFolder}'
        python = '${workspaceFolder}/.venv/Scripts/python.exe'
    }

    if ($type -eq 1) {
        $config['jinja'] = $true
    }

    if ($isFlask) {
        if ($runType -eq 0) {
            $config.name = 'Flask: dev'
            $config.module = 'flask'
            $config.args = @('--app', $mainDisplay, 'run', '--debug')
        }
        else {
            $config.name = 'Flask: Python'
            $config.program = '${workspaceFolder}/' + $mainDisplay
        }
    }
    else {
        if ($runType -eq 0) {
            $config.name = 'FastAPI: dev'
            $config.module = 'fastapi'
            $config.args = @('dev', $mainDisplay)
        }
        elseif ($runType -eq 1) {
            $config.name = 'FastAPI: Uvicorn'
            $config.module = 'uvicorn'
            $config.args = @($appImport, '--reload')

            if (-not $usePackage) {
                $config.args += @('--app-dir', 'src')
            }
        }
        else {
            $config.name = 'FastAPI: Python'
            $config.program = '${workspaceFolder}/' + $mainDisplay
        }
    }

    $vscodeFolder = Join-Path (Get-Location).Path '.vscode'
    $launchFile = Join-Path $vscodeFolder 'launch.json'

    if (-not (Test-Path -LiteralPath $launchFile)) {
        if (-not (Test-Path -LiteralPath $vscodeFolder)) {
            New-Item -ItemType Directory -Path $vscodeFolder | Out-Null
        }

        $launch = @{
            version = '0.2.0'
            configurations = @($config)
        }

        $launch | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $launchFile -Encoding UTF8
        Write-Host 'Created .vscode/launch.json for VS Code.' -ForegroundColor Green
    }
    else {
        Write-Host '.vscode/launch.json already exists, so it was not overwritten.' -ForegroundColor Yellow
    }
}

if (-not (Test-Path -LiteralPath (Join-Path $scriptsFolder 'python.exe'))) {
    Write-Host 'Could not find Python inside .venv.' -ForegroundColor Red
    return
}

if ($env:VIRTUAL_ENV -eq $venv) {
    Write-Host 'This environment is already active.'
}
elseif ($env:VIRTUAL_ENV) {
    Write-Host 'Another environment is active. Run deactivate first.' -ForegroundColor Yellow
    return
}
else {
    $oldPrompt = Get-Command prompt -CommandType Function -ErrorAction SilentlyContinue

    $global:LazySaved = @{
        Path = $env:Path
        PythonHome = $env:PYTHONHOME
        VirtualEnvPrompt = $env:VIRTUAL_ENV_PROMPT
        Prompt = $null
    }

    if ($oldPrompt) {
        $global:LazySaved.Prompt = $oldPrompt.ScriptBlock
    }

    $env:VIRTUAL_ENV = $venv
    $env:VIRTUAL_ENV_PROMPT = '.venv'
    $env:Path = "$scriptsFolder;$env:Path"
    Remove-Item Env:PYTHONHOME -ErrorAction SilentlyContinue

    function global:prompt {
        Write-Host -NoNewline '(.venv) ' -ForegroundColor Green

        if ($global:LazySaved.Prompt) {
            & ($global:LazySaved.Prompt)
        }
        else {
            "PS $($PWD.Path)> "
        }
    }

    function global:deactivate {
        if (-not $global:LazySaved) {
            return
        }

        $env:Path = $global:LazySaved.Path
        Remove-Item Env:VIRTUAL_ENV -ErrorAction SilentlyContinue

        if ($global:LazySaved.PythonHome) {
            $env:PYTHONHOME = $global:LazySaved.PythonHome
        }
        else {
            Remove-Item Env:PYTHONHOME -ErrorAction SilentlyContinue
        }

        if ($global:LazySaved.VirtualEnvPrompt) {
            $env:VIRTUAL_ENV_PROMPT = $global:LazySaved.VirtualEnvPrompt
        }
        else {
            Remove-Item Env:VIRTUAL_ENV_PROMPT -ErrorAction SilentlyContinue
        }

        if ($global:LazySaved.Prompt) {
            Set-Item Function:global:prompt $global:LazySaved.Prompt
        }
        else {
            Remove-Item Function:global:prompt -ErrorAction SilentlyContinue
        }

        Remove-Variable LazySaved -Scope Global
        Remove-Item Function:global:deactivate
    }

    Write-Host 'Virtual environment activated!' -ForegroundColor Green
    Write-Host 'Type deactivate when finished.'
}

if ($isFramework) {
    Write-Host ''

    if ($isFastAPI) {
        Write-Host 'Run your FastAPI app with:' -ForegroundColor Cyan

        if ($runType -eq 0) {
            Write-Host "  fastapi dev $mainDisplay" -ForegroundColor Green
        }
        elseif ($runType -eq 1) {
            if ($usePackage) {
                Write-Host "  uvicorn $appImport --reload" -ForegroundColor Green
            }
            else {
                Write-Host '  uvicorn main:app --reload --app-dir src' -ForegroundColor Green
            }
        }
        else {
            Write-Host "  python $mainDisplay" -ForegroundColor Green
        }
    }
    else {
        Write-Host 'Run your Flask app with:' -ForegroundColor Cyan

        if ($runType -eq 0) {
            Write-Host "  flask --app $mainDisplay run --debug" -ForegroundColor Green
        }
        else {
            Write-Host "  python $mainDisplay" -ForegroundColor Green
        }
    }

    Write-Host 'In VS Code, select the app launch configuration and press F5.' -ForegroundColor Cyan
    if ($place -eq 1) {
        Write-Host 'Open the new project folder in VS Code first (File > Open Folder).' -ForegroundColor Yellow
    }
}

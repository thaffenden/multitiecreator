function ActivateEnvrionment {
    Invoke-Expression "cd .\project"
    Invoke-Expression "python -m venv ."
    Write-Host "Restoring virtual python environment ... please wait..."
    Invoke-Expression ".\Scripts\Activate.ps1"
}

function InstallRequirements {
    Invoke-Expression "pip install -r requirements.txt"
}

function ShowUI {
    Invoke-Expression ".\CreateUI.py"
}

function LaunchProcess {

    ActivateEnvrionment
    InstallRequirements
    ShowUI
}

LaunchProcess

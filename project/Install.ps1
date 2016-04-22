function Download-Python {
    $version = "3.5.1"
    $exename = "python-$version-amd64-webinstall.exe"
    $url = "https://www.python.org/ftp/python/$version/$exename"
    $destination = "$env:userprofile\Downloads\$exename"

    if (!(Test-Path $destination)) {
        Write-Host "Downloading Python" -ForegroundColor Yellow
        Invoke-WebRequest $url -OutFile $destination

        # double check that is was written to disk
        if(!(Test-Path $destination)){
            throw 'Unable to download python'
        }
    
    }
    return $destination
}

function Install-Python([string]$path) {
    Start-Process -FilePath $path -ArgumentList "/quiet", "PrependPath=1"
    Write-Host "Python installed" -ForegroundColor Green
    Write-Host "Validating path variable..."

    Start-Sleep -s 5

    $installdir = "$env:userprofile\AppData\Local\Programs\Python\"

    if (!(Test-Path $installdir))
    {
        Start-Sleep -s 10
    }
    $pythonversion = Get-ChildItem $installdir

    Write-Host "Python Folder: $pythonversion"

    $env:Path += ";$installdir$pythonversion"
    $env:Path += ";$installdir$pythonversion\Scripts"

    Write-Host ([Environment]::GetEnvironmentVariable("PATH")) -ForegroundColor Yellow
    Write-Host "Verified Python path" -ForegroundColor Green
    return "$installdir\Python35"
}

function InstallVirtualenv {
    Invoke-Expression "pip install virtualenv"
}

function Create-Environment {
    Write-Host "Creating Virtual Environment" -ForegroundColor Yellow
    Invoke-Expression "cd .\project\"
    Invoke-Expression "virtualenv ."
    Invoke-Expression ".\Scripts\Activate.ps1"
    Invoke-Expression "pip install -r requirements.txt"
    Write-Host "Packages installed in environment" -ForegroundColor Green
}

function Copy-tcl-files([string]$pythonlocation) {
    Write-Host "Python Install Location: $pythonlocation"
    $curdir = Convert-Path .
    Copy-Item "$pythonlocation\tcl\*" "$curdir\tcl\"
    Write-Host "Copied UI Files"

}

function Install-Requirements {
    $python = Download-Python
    $installlocation = Install-Python $python

    Write-Host "Initialising pip" -ForegroundColor Yellow
    Start-Sleep -s 60
    InstallVirtualenv

    Write-Host "All required components installed" -ForegroundColor Green

    Create-Environment
    Copy-tcl-files $installlocation

}

Install-Requirements
 
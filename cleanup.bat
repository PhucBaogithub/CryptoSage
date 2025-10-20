@echo off
REM CryptoSage - Cleanup Script for Windows
REM Xoá tất cả các file không cần thiết

setlocal enabledelayedexpansion

REM Colors (ANSI)
set "BLUE=[34m"
set "GREEN=[32m"
set "YELLOW=[33m"
set "NC=[0m"

echo.
echo %BLUE%╔════════════════════════════════════════════════════════════╗%NC%
echo %BLUE%║              CryptoSage - Cleanup Script                   ║%NC%
echo %BLUE%╚════════════════════════════════════════════════════════════╝%NC%
echo.

set "DELETED=0"

echo %YELLOW%🧹 Cleaning up project...%NC%
echo.

REM Delete __pycache__ directories
for /d /r . %%d in (__pycache__) do (
    if exist "%%d" (
        echo %GREEN%✓%NC% Deleting: %%d
        rmdir /s /q "%%d" >nul 2>&1
        set /a DELETED+=1
    )
)

REM Delete .pytest_cache directories
for /d /r . %%d in (.pytest_cache) do (
    if exist "%%d" (
        echo %GREEN%✓%NC% Deleting: %%d
        rmdir /s /q "%%d" >nul 2>&1
        set /a DELETED+=1
    )
)

REM Delete *.pyc files
for /r . %%f in (*.pyc) do (
    if exist "%%f" (
        echo %GREEN%✓%NC% Deleting: %%f
        del /q "%%f" >nul 2>&1
        set /a DELETED+=1
    )
)

REM Delete *.pyo files
for /r . %%f in (*.pyo) do (
    if exist "%%f" (
        echo %GREEN%✓%NC% Deleting: %%f
        del /q "%%f" >nul 2>&1
        set /a DELETED+=1
    )
)

REM Delete *.log files
for /r . %%f in (*.log) do (
    if exist "%%f" (
        echo %GREEN%✓%NC% Deleting: %%f
        del /q "%%f" >nul 2>&1
        set /a DELETED+=1
    )
)

REM Delete *.tmp files
for /r . %%f in (*.tmp) do (
    if exist "%%f" (
        echo %GREEN%✓%NC% Deleting: %%f
        del /q "%%f" >nul 2>&1
        set /a DELETED+=1
    )
)

REM Delete Thumbs.db
for /r . %%f in (Thumbs.db) do (
    if exist "%%f" (
        echo %GREEN%✓%NC% Deleting: %%f
        del /q "%%f" >nul 2>&1
        set /a DELETED+=1
    )
)

echo.
echo %GREEN%╔════════════════════════════════════════════════════════════╗%NC%
echo %GREEN%║                  ✓ Cleanup Complete!                       ║%NC%
echo %GREEN%╚════════════════════════════════════════════════════════════╝%NC%
echo.
echo %BLUE%Summary:%NC%
echo   %GREEN%✓%NC% Total items deleted: !DELETED!
echo.
echo %YELLOW%💡 Tips:%NC%
echo   • Run this script regularly to keep project clean
echo   • Safe to run - only deletes cache and temporary files
echo   • Does not delete source code or data
echo.

pause


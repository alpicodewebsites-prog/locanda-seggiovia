@echo off
chcp 65001 >nul
setlocal

echo ============================================================
echo  Locanda Seggiovia - caricamento del progetto su GitHub
echo ============================================================
echo.
echo Questo script fa tre cose:
echo   1. cancella la credenziale GitHub salvata (danielegremes-spec)
echo   2. avvia il caricamento del progetto
echo   3. Git aprira' una finestra nel browser: accedi come
echo      alpicodewebsites-prog e autorizza
echo.
echo Premi un tasto per cominciare.
pause >nul

cd /d "%~dp0"

echo.
echo --- 1. Rimuovo la credenziale GitHub precedente ---
cmdkey /delete:LegacyGeneric:target=git:https://github.com >nul 2>&1
if %errorlevel%==0 (
  echo     credenziale rimossa
) else (
  echo     nessuna credenziale da rimuovere, oppure gia' assente
)

echo.
echo --- 2. Carico il progetto (potrebbe chiederti di accedere) ---
git push -u origin main

if %errorlevel%==0 (
  echo.
  echo ============================================================
  echo  FATTO - il progetto e' su GitHub
  echo ============================================================
) else (
  echo.
  echo ============================================================
  echo  NON RIUSCITO - leggi il messaggio qui sopra
  echo ============================================================
  echo.
  echo Se dice "Authentication failed", ripeti: la finestra di
  echo accesso potrebbe essersi chiusa senza completare il login.
)

echo.
echo Premi un tasto per chiudere.
pause >nul

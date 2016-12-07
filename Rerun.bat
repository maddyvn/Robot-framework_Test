@echo OFF
cls
:: CLEAN UP PREVIOUS REPORTS
del /f /q /s Report\*.*

:: FIST RUN TEST
echo:
echo #### First run tests
cmd /c pybot -d Report -o output.xml -i Rerun Test

:: LOGICAL CHECK FOR RERUN FAIL TEST
if errorlevel 1 goto DGTFO
echo:
echo #### All tests passed
exit /b
:DGTFO

:: SECOND RUN FOR FAIL TEST
echo:
echo #### Rerun failed tests
cmd /c pybot -d Report -R Report\output.xml -o rerun.xml -i Rerun Test

:: MERGE TEST RESULTS
echo:
echo #### Merge tests
cmd /c rebot -d Report -o output.xml --merge Report\output.xml Report\rerun.xml
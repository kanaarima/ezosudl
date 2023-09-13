@echo off
set /A osufolder=c:\osu
echo %osufolder%
python3 main.py -l=beatmapsets.txt -o=%osufolder% -s=%osufolder%\Songs
pause
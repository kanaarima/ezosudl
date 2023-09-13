@echo off
set /A osufolder=c:\osu
python3 main.py -l=beatmapsets.txt -o=%osufolder% -s=%osufolder%\Songs
pause
@echo off
set  osufolder=c:\osu
python3 main.py -l=beatmapsets.txt -o=%osufolder% -s=%osufolder%\Songs
pause
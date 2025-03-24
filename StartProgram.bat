@echo off
cd /d "C:\Coding\Python\TwitchClipFetcher"
git pull
start cmd /k "py -m src.main"

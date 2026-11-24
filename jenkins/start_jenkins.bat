@echo off
chcp 65001 >nul
cd /d %~dp0
if not exist logs mkdir logs
echo Uruchamianie Jenkinsa (pierwszy raz kilka minut)...
echo $ docker compose up -d --build > logs\01_compose_up.txt
docker compose up -d --build >> logs\01_compose_up.txt 2>&1
echo.>> logs\01_compose_up.txt
echo $ docker compose ps >> logs\01_compose_up.txt
docker compose ps >> logs\01_compose_up.txt 2>&1
echo Gotowe. Jenkins: http://localhost:8080
timeout /t 10

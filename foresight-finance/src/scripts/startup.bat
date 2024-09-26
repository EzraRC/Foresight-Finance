@echo off

REM Start the Vue development server
start npm run serve

REM Start the HTTP server
start python -m http.server 8080

REM Start the candlestick update loop
:loop
python candlestick_graph.py
timeout /t 60
goto loop
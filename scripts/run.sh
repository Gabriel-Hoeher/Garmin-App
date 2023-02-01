#! /bin/bash 

bash ./fitToCsv.sh
wait

python3 multiAnalyzer.py
wait

# invokes windows b/c wsl doesn't support graphics
cmd.exe /C start http://localhost:7100

# START server 
cd ../server
nodemon
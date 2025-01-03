# cd /home/ubuntu/Server/
# git pull 
# sudo systemctl stop myapp
# sudo systemctl daemon-reload
# sudo systemctl start myapp
# sudo systemctl enable myapp

# This will Refresh the Server Running Clearing the output of Previous Run and 
cd ~/Application-Server/

git pull

PID=$(lsof -t -i:5001)

# If the PID exists, kill the process
if [ -n "$PID" ]; then
    echo "Stopping Gunicorn server with PID: $PID"
    kill -9 $PID
    echo "Gunicorn server stopped"
else
    echo "No Gunicorn process found on port 5001"
fi

# Restart the Gunicorn server
echo "Starting Gunicorn server..."

echo "============================================" >> output.log
echo "Gunicorn server started at: $(date '+%Y-%m-%d %H:%M:%S')" >> output.log
echo "============================================" >> output.log
nohup /home/ayush/.pyenv/versions/3.10.13/envs/test/bin/gunicorn -b 0.0.0.0:5001 --access-logfile - app:app >> output.log 2>&1 &
echo "Gunicorn server started"
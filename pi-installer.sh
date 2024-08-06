#!/bin/bash

BOT_SCRIPT="bot.py"
USER=$(whoami)
PYTHON_VERSION="python3"
VENV_DIR="venv"
SCRIPT_DIR="/home/$USER/scripts"
BOT_DIR="/home/$USER/Desktop/discord-bot-journal"
CRON_JOB_FILE="/home/$USER/scripts/manage_bot.sh"
RTCWAKE_TIME_ON="18:00"


# Install necessary packages
sudo apt update
sudo apt install -y $PYTHON_VERSION python3-pip git cron rtcwake

# Create and activate virtual environment
$PYTHON_VERSION -m venv $VENV_DIR
source $VENV_DIR/bin/activate
pip install -r requirements.txt

# Create the script directory if it doesn't exist
mkdir -p $SCRIPT_DIR

# Create the manage_bot.sh script
cat <<EOF > $CRON_JOB_FILE
#!/bin/bash

# Path to your Python script
BOT_SCRIPT="$BOT_DIR/$BOT_SCRIPT"

# Start the Python script
start_script() {
    echo "Starting Python script..."
    $VENV_DIR/bin/python3 \$BOT_SCRIPT &
    # Save the process ID (PID) to a file
    echo \$! > /tmp/my_bot_script.pid
}

# Stop the Python script
stop_script() {
    if [ -f /tmp/my_bot_script.pid ]; then
        PID=\$(cat /tmp/my_bot_script.pid)
        echo "Stopping Python script with PID \$PID..."
        kill \$PID
        rm /tmp/my_bot_script.pid
    else
        echo "No PID file found. Script might not be running."
    fi
}

# Check current hour
CURRENT_HOUR=\$(date +'%H')
if [ \$CURRENT_HOUR -ge 18 ] && [ \$CURRENT_HOUR -lt 23 ]; then
    start_script
else
    stop_script
    echo "Putting Raspberry Pi to sleep..."
    sudo rtcwake -m mem -l -t \$(date +%s -d '5 minutes')
fi
EOF

# else
    # stop_script
    # echo "Putting Raspberry Pi to sleep..."
    # sudo rtcwake -m off -l -t \$(date +%s -d tomorrow$RTCWAKE_TIME_ON)
# fi

# Make the manage_bot.sh script executable
chmod +x $CRON_JOB_FILE

# Create a cron job to handle the bot script and rtcwake
(crontab -l 2>/dev/null; echo "0 18 * * * $CRON_JOB_FILE") | crontab -
(crontab -l 2>/dev/null; echo "0 23 * * * $CRON_JOB_FILE") | crontab -

# Create a cron job to wake the Raspberry Pi at 6 PM Central Time everyday
(crontab -l 2>/dev/null; echo "0 18 * * * sudo rtcwake -m no -l -t \$(date +%s -d today$RTCWAKE_TIME_ON)") | crontab -

# Ensure the bot script runs at reboot (in case of unexpected reboots)
(crontab -l 2>/dev/null; echo "@reboot $CRON_JOB_FILE") | crontab -

echo "Cron jobs set up successfully."

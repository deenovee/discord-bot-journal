#!/bin/bash

BOT_SCRIPT="bot.py"
USER=$(whoami)
PYTHON_VERSION="python3"
VENV_DIR="venv"
SCRIPT_DIR="/home/$USER/scripts"
BOT_DIR="/home/$USER/Desktop/discord-bot-journal"
CRON_JOB_FILE="/home/$USER/scripts/manage_bot.sh"
ON_START_FILE="/home/$USER/scripts/on_start.sh"


# Install necessary packages
sudo apt update
sudo apt install -y $PYTHON_VERSION python3-pip git cron

# Create and activate virtual environment
$PYTHON_VERSION -m venv $VENV_DIR
source $VENV_DIR/bin/activate
pip install -r requirements.txt

# Create the script directory if it doesn't exist
mkdir -p $SCRIPT_DIR

# Create the manage_bot.sh script
cat <<EOF > $CRON_JOB_FILE
#!/bin/bash

if [ -f /tmp/my_bot_script.pid ]; then {
    PID=\$(cat /tmp/my_bot_script.pid)
    echo "Stopping bot with PID \$PID..."
    kill \$PID
}
else
    echo "Bot is not running."
fi

echo +68400 | sudo tee /sys/class/rtc/rtc0/wakealarm

sudo halt
EOF

cat <<EOF > $ON_START_FILE

USER=$(whoami)

cd /home/$USER/Desktop/discord-bot-journal

python3 bot.py &
echo $! > /tmp/my_bot_script.pid

while true; do
    sleep infinity
done

EOF

chmod +x $CRON_JOB_FILE

(crontab -l 2>/dev/null; echo "0 4 * * * $CRON_JOB_FILE") | crontab -

echo "Cron jobs set up successfully."

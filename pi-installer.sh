#!/bin/bash

# Variables
DOMAIN="example.com"
BOT_REPO="github.com/discord-journal-bot.git"
BOT_DIR="./discord-journal-bot"
BOT_SCRIPT="bot.py"
USER=$(whoami)
PYTHON_VERSION="python3"
VENV_DIR="venv"

# Update and upgrade the system
sudo apt update && sudo apt upgrade -y

# Install necessary packages
sudo apt install -y $PYTHON_VERSION python3-pip nginx git ufw certbot python3-certbot-nginx

# Clone the bot repository
git clone $BOT_REPO 
cd $BOT_DIR

# Create a virtual environment and install dependencies
$PYTHON_VERSION -m venv $VENV_DIR
source $VENV_DIR/bin/activate
pip install -r requirements.txt

# Create Nginx configuration for the bot
sudo bash -c "cat > /etc/nginx/sites-available/discord_bot <<EOL
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOL"

# Enable the Nginx configuration
sudo ln -s /etc/nginx/sites-available/discord_bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Obtain SSL certificate
sudo certbot --nginx -d $DOMAIN

# Create a systemd service for the bot
sudo bash -c "cat > /etc/systemd/system/discord_bot.service <<EOL
[Unit]
Description=Discord Bot
After=network.target

[Service]
User=$USER
WorkingDirectory=$HOME/$BOT_DIR
ExecStart=$HOME/$BOT_DIR/$VENV_DIR/bin/python $HOME/$BOT_DIR/$BOT_SCRIPT
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOL"

# Enable and start the bot service
sudo systemctl enable discord_bot
sudo systemctl start discord_bot

# Configure firewall
sudo ufw allow 'Nginx Full'
sudo ufw enable

echo "Setup complete. Your Discord bot should now be running and accessible."

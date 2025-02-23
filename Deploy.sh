#!/bin/bash

GIT_REPO = "git@github.com:vjghoslya/ci-cd-pileline-tool.git"
PROD_DIR = "/var/www/html"
BRANCH = "main"

if [ -d "$PROD_DIR" ]; then
    echo "Repository exists. Pulling latest changes..."
    cd "$PROD_DIR" || exit
    git reset --hard origin/$BRANCH  # Reset to remote to avoid conflicts
    git pull origin $BRANCH
else
    echo "Cloning repository..."
    git clone -b $BRANCH $GIT_REPO $PROD_DIR
    cd "$PROD_DIR" || exit
fi

# Restart Nginx
echo "Restarting Nginx..."
sudo systemctl restart nginx

echo "Deployment completed!"
#!/bin/bash

git pull --force

pip3 install discord.py[voice]
pip3 install requests
pip3 install mcstatus

read -p "Please download https://www.datendieter.de/item/Liste_von_deutschen_Staedtenamen_.csv as staedte_osm.txt || Press Enter to continue"
read -p "Please download https://www.datendieter.de/item/Liste_von_deutschen_Strassennamen_.csv as strassen_osm.txt || Press Enter to continue"

read -sp "Please input your bot token: " token
echo ""
read -p "Please input you discord user ID: " uid
echo ""
read -p "Please input the desired bot prefix: " prefix

echo '{"token": "'$token'", "owner_id": '$uid', "prefix": "'$prefix'"}' > config.json

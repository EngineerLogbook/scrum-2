#!/usr/bin/env bash

echo "Media backup initiated on $(date +'%m|%d|%Y-%I:%M%p')" >> /var/log/cron.log 2>&1

rclone sync  /usr/src/app/media/ logdrive:Backups/media >> /var/log/cron.log 2>&1


echo "Media files synced with google drive"  >> /var/log/cron.log 2>&1
#!/usr/bin/env bash

echo "Database backup initiated on $(date +'%m|%d|%Y-%I:%M%p')" >> /var/log/cron.log 2>&1

docker exec -i log_database pg_dumpall -c -U boileruser > /postgres.dbdump.sql
rclone copy /postgres.dbdump.sql logdrive:Backups/database >> /var/log/cron.log 2>&1

echo "Database backup complete"  >> /var/log/cron.log 2>&1

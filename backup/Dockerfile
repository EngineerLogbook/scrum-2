FROM ubuntu:latest

# Install dependencies
RUN apt-get update && apt-get install docker.io cron tree rclone ca-certificates -y

# Install the crontab
ADD crontab /etc/cron.d/backup-server

# Install rclone config file
ADD rclone.conf /root/.config/rclone/rclone.conf

# Mount media and database volumes
ADD media.sh /media.sh
ADD db.sh /db.sh

# Change file permissions
RUN chmod +x /media.sh /db.sh /etc/cron.d/backup-server

# Create the log file to be able to run tail
RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log

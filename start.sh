#!/bin/sh
mkdir -p /var/run/sshd
mkdir -p /root/.ssh/ 
chmod 600 ~/.ssh
chmod 600 /etc/ssh/*
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
echo $SSH_KEY > /root/.ssh/authorized_keys

# Write image to disk
sudo dd bs=1m if=2017-09-07-raspbian-stretch-lite.img of=/dev/rdisk2 conv=sync

# Enable SSH
sudo systemctl enable ssh
sudo systemctl start ssh

# Copy and paste client.ovpn to conf/client.ovpn

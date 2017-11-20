# I'll get around to doing this

#delete lines
sudo sh -c "sed '1,100d' apt-updates.log > apt-updates.log"

#get line count
wc -l <filename>
Utilizes graph-tool
http://projects.skewed.de/graph-tool/

For Ubuntu 11.04

Add these lines to /etc/apt/sources.list

deb http://downloads.skewed.de/apt/natty natty universe
deb-src http://downloads.skewed.de/apt/natty natty universe

apt-get upgrade
apt-get install graph-tool


Utilizes geopy

sudo easy_install geopy
OR
svn co http://geopy.googlecode.com/svn/trunk/ geopy-trunk
cd geopy-trunk/
sudo python setup.py install




INSTRUCTIONS (Make sure above two packages are installed)

Input a starting address in Bellingham
Format: 501 Voltaire Ct in Bellingham

Input an ending address in Bellingham
Format: Bellis Fair Mall in Bellingham

Input a time in 24hr format
Format: 14:30

The algorithm then returns the top 3 fastest bus routes to your destination [if it's lucky ;) ].

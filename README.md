## Shodan Bulk IP LookUp

Uses Shodan's Python library to perform bulk lookup of IPs. Converts the default Shodan JSON to CSV.

Shodan API key required. If you only have a basic Shodan API this script can burn through it pretty quickly as well as hitting the rate limit very rapidly.

### Installation

``````
git clone https://github.com/nixintel/BulkShodan

cd BulkShodan

pip install -r requirements.txt

``````

Be sure to enter your own API key in the ```.env``` file.

### Usage

The script takes input from a list of IP addresses in a file. CIDR notation is supported.

Output is as a CSV.

Example input file:

``````
iplist.txt:

x.x.x.x
y.y.y.y/27
z.z.z.z/24
``````

Usage:

``````
python main.py -i iplist.txt -o shodan_data.csv
``````

The script is still under development, so use at your own risk!

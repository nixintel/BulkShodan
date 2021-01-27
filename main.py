import shodan
import settings as s
import ipaddress
import argparse
import pandas as pd

pd.set_option('display.max_columns', 500)


def get_ipv4_list(multi_ips):
    """Formats IP addresses inputted as a list. Converts CIDR to list of single IPs"""

    ip_list = []

    with open(multi_ips, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        lines = [x for x in lines if x]

    for i in lines:
        net = ipaddress.ip_network(i, strict=False)
        for n in net:
            ipv4 = format(ipaddress.IPv4Address(n))
            ip_list.append(ipv4)

    return ip_list


def shodan_query(api_key,ip):
    """Takes IP as input, queries Shodan and returns host info as JSON"""

    api = shodan.Shodan(api_key)
    responses = []

    try:
        for i in ips:
            result = api.host(i)
            print('Querying Shodan for ' + str(i))
            responses.append(result)

    except Exception as e:
        print('Error %s' %e)

    return responses


def shodan_df(raw_data):
    """Organises raw Shodan results into DataFrame"""

    df = pd.DataFrame(raw_data, index=None)
    df = pd.json_normalize(raw_data, ['data'], errors='ignore')

    # Rearrange columns so ip_str is first
    df = df.drop(['ip', 'http.html'], axis=1)
    lead_col = ['ip_str']
    new_cols = lead_col + (df.columns.drop(lead_col).tolist())
    df = df[new_cols]

    print(df.head())

    return df


def create_csv(df, filename):
    """Converts Dataframe to CSV"""

    print('Creating CSV...')
    filename = str(filename)
    report = df.to_csv(filename, index=True)
    print('Report saved to ' + filename)
    return report


def get_args():
    """Takes arguments to set input/output file"""

    return args


if __name__ == "__main__":

    # Set API key
    key = s.shodan_key

    # Arguments

    parser = argparse.ArgumentParser(description='Queries Shodan for multiple IPs, returns CSV')
    parser.add_argument('-i', '--input',
                        help='specify a list of IP addresses / CIDR from a file (one IP per line).', type=str,
                        required=True)
    parser.add_argument('-o', '--output', help='Output file. Select filename and path for results csv', type=str,
                        required=True)
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output

    # Main

    ips = get_ipv4_list(input_file)
    shodan_results = shodan_query(key, ips)
    dataframe = shodan_df(shodan_results)
    create_csv(dataframe, output_file)






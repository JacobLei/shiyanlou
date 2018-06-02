
import re
from datetime import datetime

def open_parser(filename):
    with open(filename) as logfile:
        pattern = (r''
                   r'(\d+.\d+.\d+.\d+)\s-\s-\s'     # ip
                   r'\[(.+)\]\s'                    # time
                   r'"GET\s(.+)\s\w+/.+"\s'         # path
                   r'(\d+)\s'                       # status code
                   r'(\d+)\s'                       # size of data 
                   r'"(.+)"\s'                      # head
                   r'"(.+)"'                        # client info
                   )
        parsers = re.findall(pattern, logfile.read())
    return parsers

def main():
    logs = open_parser('/home/shiyanlou/Code/nginx.log')
    ip_times_dict = {}
    url_404_dict = {}
    for log in logs:
        time, _ = log[1].split(' ')
        date = datetime.strptime(time, '%d/%b/%Y:%H:%M:%S')
        if date.day == 11:
            if log[0] in ip_times_dict.keys():
                ip_times_dict[log[0]] += 1
            else:
                ip_times_dict[log[0]] = 1
        if log[3] == '404':
            if log[2] in url_404_dict.keys():
                url_404_dict[log[2]] += 1
            else:
                url_404_dict[log[2]] = 1
    key, value = sorted(ip_times_dict.items(), key=lambda d: d[1], reverse=True)[0]
    ip_dict = {key : value}
    key, value = sorted(url_404_dict.items(), key=lambda d: d[1], reverse=True)[0]
    url_dict = {key : value}
    return ip_dict, url_dict

if __name__ == '__main__':
    ip_dict, url_dict = main()
    print(ip_dict, url_dict)

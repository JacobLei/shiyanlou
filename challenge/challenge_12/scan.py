
import sys
import re
import socket
from getopt import getopt, GetoptError

class Args(object):

    def __init__(self):
        self.options = self._options()

    def _options(self):
        try:
            opts, _ = getopt(sys.argv[1:], 'h:p:', ['host=', 'port=']) 
        except GetoptError:
            print('Parameter Error')
            exit()
        options = dict(opts)
        if len(options) != 2:
            print('Parameter Error')
            exit()
        return options

    def _value_after_options(self, option):
        value = self.options[option]
        if value is None:
            print('Parameter Error')
            exit()
        return value

    def host(self):
        host = self._value_after_options('--host')
        if not re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', host):
            print('Parameter Error')
            exit()
        return host

    def ports(self):
        port = self._value_after_options('--port')
        ports = port.split('-')
        if len(ports) == 1:
            try:
                ports = [int(ports[0])]
            except ValueError:
                print('Parameter Error')
        elif len(ports) == 2:
            try:
                ports = [x for x in range(int(ports[0]), int(ports[-1])+1)]
            except ValueError:
                print('Parameter Error')
        else:
            print('Parameter Error')
            exit()
        return ports

def IsOpen(host, port):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(0.1)
    try:
        sk.connect((host, port))
        ret = True
    except Exception:
        ret = False
    sk.close()
    return ret

args = Args()

if __name__ == '__main__':
    host = args.host()
    ports = args.ports()
    for port in ports:
        if IsOpen(host, port):
            print('{} open'.format(port))
        else:
            print('{} closed'.format(port))






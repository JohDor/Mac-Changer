import subprocess
import optparse
import re

def get_arguments():
    # using parser and opt parse to parse the entries
    parser = optparse.OptionParser()
    # gives options when run on linux
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="new MAC address")
    (options, arguments) = parser.parse_args()
    # returns the arguments of all options which have been parsed so interface and new_mac
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info.")
    return options

def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    # using subprocess.call(["", ,""]) format to limit the arguments available for input
    #turns off interface
    subprocess.call(["ifconfig", interface, "down"])
    #chhanges interface
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    #turns on interface
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    #returns alphanumeric
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        #returns none type
        print("[-] Could not get MAC address")

#starts program
options = get_arguments()
#starts the change
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))
# calls from the get_arguments options
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
#cast to string because it could return as none type
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed")

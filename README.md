# The Land of No Return (LONR)
This is a rebirth of the old Apple //e BBS software that was written and maintained by Dmitri Baughman.  It operated in the mid '80s in Salt Lake City, UT.  LONR was a heavily modified Applesoft BASIC program based on [The Proving Grounds BBS software](https://bbs.fandom.com/wiki/Proving_Grounds) written for the [Apple Cat II modem](https://wikivisually.com/wiki/Novation_CAT#The_Apple-CAT_II) by Mike Heinstein, aka The Timelord.

## Running the Server
```diff
- IMPORTANT - Python >= 3.6.7 is required!
```
1. Update your system `sudo apt update && sudo apt upgrade` (Ubuntu systems)
2. Get the repo `git clone https://github.com/slyderc/lonr.git`
3. CD into 'lonr' and install the server with `sudo ./installer.sh`

#### If you want to add a firewall which only allows logins via ssh or telnet:

`sudo cp /opt/lonr/firewall.nft /etc/firewall.conf`

`sudo apt -y install nftables`

`sudo nft -f /etc/firewall.conf`

`sudo echo '#!/bin/sh' > /etc/network/if-up.d/firewall`

`sudo echo 'nft flush ruleset' >> /etc/network/if-up.d/firewall`

`sudo echo 'nft -f /etc/firewall.conf' >> /etc/network/if-up.d/firewall`

`sudo chmod +x /etc/network/if-up.d/firewall`

#### You now should be able to telnet to your server at `<server IP/hostname>:7777`


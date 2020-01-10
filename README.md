Script used to buy products from chosen auctions on Allegro.pl
Based on selenium.
In order to execute script:
0.Run AllegroGetAcessToken.py in order to get all credentials needed for allegro api (you have to run it only once)
1.Download geckodriver for firefox from: https://github.com/mozilla/geckodriver/releases
2.Extract and unzip and move the geckodriver file to /usr/local/bin/ directory if on linux
or if on windows add geckodriver to environment variables. as per instruction: https://www.youtube.com/watch?v=KNzGtHI_60o
3.Use 'pip install -r requirements.txt' command in order to install all dependencies.
4.Download and install openvpn including gui: https://openvpn.net/community-downloads/
5.If you want to use nordvpn as vpn provider, download all available configs for openvpn from: https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip
6.Extract configs to C:\Program Files\OpenVPN\config [you don't need all of them, usually one per account plus 5 as backup]
7.In order to skip the login prompt every time you change ip:
 I.Create new file named login.conf and then add your clients username and password
     username
     password
 II.Add this line to your openvpn clients config file manually:
    auth-user-pass login.conf
    Or run 'add_credentials_to_config_files.py' to let script handle it.

In order for script to work:
1.If reading from file split each auction number by enter.
2.If you chose to modify prices before buying, list of auctions must contain only auctions from single allegro account
ex. if you chose account 'czemutaktanio', list must contain auctions from this account.
3.In order to add accounts that are making purchase, add entry to accounts.json.
Every account needs vpn config in order to change ip before sale.
All available configs should be found C:\Program Files\OpenVPN\config
All logins needs a password added to keyring using command in cmd:
    keyring set allegro PASSWORD
where PASSWORD is a password for that login

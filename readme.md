Script used to buy products from chosen auctions
on Allegro.pl
Based on selenium.
In order to execute script:
1. Download geckodriver for firefox from: https://github.com/mozilla/geckodriver/releases
2. Extract and unzip and move the geckodriver file to /usr/local/bin/ directory if on linux
or if on windows add geckodriver to environment variables. as per instruction: https://www.youtube.com/watch?v=KNzGtHI_60o
3.Use 'pip install -r requirements.txt' command in order to install all dependencies.
In order for script to work:
1.Make first transaction yourself, using card, saving the details.
2.If reading from file, split each auction number by enter.

# aa-concur-reimbursement-internet

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/vme0-oD118Y/0.jpg)](https://www.youtube.com/watch?v=vme0-oD118Y)

Quick proof of concept to download a bill and submit it in concur.

A crontab like the below could automate this for you:
```
0 0 21 * * do-expense.sh
```

## do-expense.sh
 - This script encapsulates all the functionality.
 - see below for explaination of the indivudal python scripts

### Usage
```
#!/bin/bash
MONTH=$(date +%B)
python3 virgin.py
pdftotext $MONTH.pdf
bill_date=$(sed -nr "s#We'll collect your payment on (.*)#\1#p" $MONTH.txt)
bill_date=$(date -d"$bill_date" +%m/%d/%Y)
python3 concur.py --bill_date $bill_date --receipt $MONTH.pdf
```

## concur.py
 - This takes a expense data, receipt, location and a vendor.
 - Some modifications may be required for your country/currency.
 - When setting up chrome and chromedriver, You will need to create a seprate profile in chrome and define it on line 22.

```
profile_location = "/home/daoneill/.config/google-chrome-beta/Profile 1"
````
 - lines 50, 51 are your login information

```
password = Path('../otpanswer/key').read_text()
token = subprocess.check_output("./getpw", cwd="../otpanswer", shell=True).decode("utf-8") 
```

### Usage
```
python3 concur.py \
    --bill_date $bill_date \
    --receipt $MONTH.pdf \
    --location "Cork, IRELAND" \
    --vendor "Virgin Media"
```

## virgin.py

- This logs into virgin media and downloads the latest bill to the downloads directory
- It then moves it into the current directory.
- The name of the file will be the current month

### Usage
```
export virgin_username="its me"
export virgin_password="l33t0r"
python3 virgin.py
```
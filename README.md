# aa-concur-reimbursement-internet

Quick proof of concept to download a bill and submit it in concur.

## do-expense.sh
```
#!/bin/bash
MONTH=$(date +%B)
python3 virgin.py
pdftotext $MONTH.pdf
bill_date=$(sed -nr "s#We'll collect your payment on (.*)#\1#p" $MONTH.txt)
bill_date=$(date -d"$bill_date" +%m/%d/%Y)
python3 concur.py --bill_date $bill_date --receipt $MONTH.pdf
```
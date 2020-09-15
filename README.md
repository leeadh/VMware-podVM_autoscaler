# podVM_autoscaler

1) git clone this repo
2) pip install pyvmomi
3) python3 hpa_autoscaler.py -s <VCENTER_FQDN> -u <YOUR_USERNAME> -p <YOUR_PASSWORD> -o 443 -mem_threshold_percent <YOUR_MEMORY_THRESHOLD>

** Example: python3 hpa_autoscaler.py -s jur01-vcenter01.acepod.com -u administrator@vsphere.local -p Password12345 -o 443 -mem_threshold_percent 20 
** Values which you can input into memory threshold : from 0 to 100. 
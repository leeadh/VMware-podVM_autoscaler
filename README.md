# podVM_autoscaler

Summary: this  python script is intended to implement the Horizontal Pod Autoscaler algorithm for podVM for the vSphere 7.0 with Kubernetes. The implemetation follows the algorithm from the official Kubernetes documents : https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/ 

1) git clone this repo
2) pip install pyvmomi
3) Do a 'kubectl vsphere login' to login into your Supervisor Cluster for vSphere 7.0 with Kubernetes (https://docs.vmware.com/en/VMware-vSphere/7.0/vsphere-esxi-vcenter-server-70-vsphere-with-kubernetes-guide.pdf: Page 84) 
4) Choose the context which you want by doing 'kubectl config use-context <YOUR_NAMEPSACE>' (https://docs.vmware.com/en/VMware-vSphere/7.0/vsphere-esxi-vcenter-server-70-vsphere-with-kubernetes-guide.pdf: Page 84)
4) python3 hpa_autoscaler.py -s <VCENTER_FQDN> -u <YOUR_USERNAME> -p <YOUR_PASSWORD> -o 443 -mem_threshold_percent <YOUR_MEMORY_THRESHOLD>


** Example: python3 hpa_autoscaler.py -s jur01-vcenter01.acepod.com -u administrator@vsphere.local -p Password12345 -o 443 -mem_threshold_percent 20 
** Values which you can input into memory threshold : from 0 to 100. 

Improvements to be done
- to automatically login into the vsphere cluster and switch context
- to create a docker file of this python script
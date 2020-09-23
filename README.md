# podVM_autoscaler

## Summary and steps ##
This  python script is intended to implement the Horizontal Pod Autoscaler algorithm for podVM for the vSphere 7.0 with Kubernetes. The implemetation follows the algorithm from the official Kubernetes documents : https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/ 

The issue at hand is that with the release of vSphere 7 with Kubernetes, horitzonal pod autoscaling is still being in development. As such, to allow podVMs to be able to automatically scale, this python script was written to address that. For now this script takes in only memory utilization and is being improved for CPU utilization in the future. 

To run this script as a standalone

1) git clone this repo
2) pip install pyvmomi
3) Do a 'kubectl vsphere login' to login into your Supervisor Cluster for vSphere 7.0 with Kubernetes (https://docs.vmware.com/en/VMware-vSphere/7.0/vsphere-esxi-vcenter-server-70-vsphere-with-kubernetes-guide.pdf: Page 84) 
4) Choose the context which you want by doing 'kubectl config use-context <YOUR_NAMEPSACE>' (https://docs.vmware.com/en/VMware-vSphere/7.0/vsphere-esxi-vcenter-server-70-vsphere-with-kubernetes-guide.pdf: Page 84)
4) export these values
```
# export VC_PASSWRD=XXXX
# export VC_USERNAME=administrator@vsphere.local
# export VC_HOST=jur01-vcenter01.acepod.com
# export VC_PORT=443
```
5) python3 hpa_autoscaler.py  -mem_threshold_percent <MEMORY_THRESHOLD> -secure <YES_OR_NO> 

#### Notes ####
- Example 1: if you want to connect securely to the vSphere hosts: 

```
python3 hpa_autoscaler.py  -mem_threshold_percent 20 -secure yes
```
- Example 2: if you want to connect insecurely to the vSphere hosts: 
```
python3 hpa_autoscaler.py  -mem_threshold_percent 20 -secure no 
```
OR 

```
python3 hpa_autoscaler.py  -mem_threshold_percent 20
```

#### Note ####: Values which you can input into memory threshold : from 0 to 100. 

Things completed
- [x] Implemented HPA algo
- [x] Implemented memory threshold
- [x] Updated to have SSL context
- [x] Updated to have insecure connection option

Improvements to be done
- [ ] to automatically login into the vsphere cluster and switch context
- [ ] to create a container of this python script

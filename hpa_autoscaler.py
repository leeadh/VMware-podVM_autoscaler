#!/usr/bin/env python

# export VC_PASSWRD=XXXX
# export VC_USERNAME=administrator@vsphere.local
# export VC_HOST=jur01-vcenter01.acepod.com
# export VC_PORT=443
# python3 hpa_autoscaler.py  -mem_threshold_percent 20 -secure yes


import sys
import os
import subprocess
import ssl
from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnectNoSSL, Disconnect, SmartConnect
from pyVim.task import WaitForTask
from tools import cli
import pandas as pd
import numpy as np

__author__ = 'Adrian Lee'


def setup_args():
    parser = cli.build_arg_parser()
    parser.add_argument('-n', '--property', default='runtime.powerState',
                        help='Name of the property to filter by')
    parser.add_argument('-v', '--value', default='poweredOn',
                        help='Value to filter with')
    parser.add_argument('-mem_threshold_percent', '--mem_threshold_percent', 
                        help='Set your desired memory threshold from 0-20')
    parser.add_argument('-secure','--secure', 
                        help='Set S if you want to connect securely')
    return cli.prompt_for_password(parser.parse_args())

def get_obj(si, root, vim_type):
    container = si.content.viewManager.CreateContainerView(root, vim_type,
                                                           True)
    view = container.view
    container.Destroy()
    return view

def hpa_algo(vms, memory_threshold_utilization):
    arr =[]
    for vm in vms:
    
        summary= vm.summary
        utilizationrate = summary.quickStats.guestMemoryUsage/summary.config.memorySizeMB
        if ("harbor" not in summary.config.name ):
            
            d = {"pod_name":summary.config.name.rsplit('-', 2)[0],"mem_utilization":utilizationrate, "type": summary.config.guestId}
            arr.append(d)
    df = pd.DataFrame(arr)
    df = df.loc[df['type'] == "crxPod1Guest"]
    print(df.sort_values('pod_name',ascending=False))
    dftemp= df.groupby('pod_name', as_index=False).sum()
    dftemp['desired_mem_utilization']=float(memory_threshold_utilization) 
    dftemp['desired_replicas'] = (dftemp['mem_utilization']/dftemp['desired_mem_utilization']).apply(np.ceil)
    dftemp['desired_replicas'] = np.round(dftemp['desired_replicas']).astype('Int64')
    d = dftemp.to_dict('records')
    return d


def main():
    args = setup_args()
    filter_key = "summary.config.guestId"
    value = "crxPod1Guest" 
    mem_threshold_input = float(args.mem_threshold_percent)/100
    memory_threshold_utilization = mem_threshold_input
    secure = args.secure
    

    #sslContext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)

    if secure == "yes" or not secure:
        sslContext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        sslContext.verify_mode = ssl.CERT_REQUIRED
        sslContext.check_hostname = True
        sslContext.load_default_certs()
        si = SmartConnect   (  host=os.getenv('VC_HOST'),
                            user=os.getenv('VC_USERNAME'),
                            pwd=os.getenv('VC_PASSWRD'),
                            port=os.getenv('VC_PORT'),
                            sslContext=sslContext)
    else:
        si = SmartConnectNoSSL   (  host=os.getenv('VC_HOST'),
                            user=os.getenv('VC_USERNAME'),
                            pwd=os.getenv('VC_PASSWRD'),
                            port=os.getenv('VC_PORT'))
    vms = get_obj(si, si.content.rootFolder, [vim.VirtualMachine])
    
    hpa_vms = hpa_algo(vms,memory_threshold_utilization)

    current_deployment = subprocess.check_output(["kubectl", "get","deployment","-o=jsonpath={.items[*].metadata.name}"]).decode().split()
    hpa_vms = [d for d in hpa_vms if d['pod_name'] in current_deployment]
    print(hpa_vms)
    for vm in hpa_vms:
        print(vm['pod_name'])
        deployment = vm['pod_name']
        replica_count = "--replicas="+str(vm['desired_replicas'])
        subprocess.call(["kubectl","scale","deployments",deployment,replica_count])

    
    

    Disconnect(si)


if __name__ == '__main__':
    main()

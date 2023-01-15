import subprocess
import argparse
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import atexit

def deploy_local(path, vmname):
    # Run the VMWare Fusion to create & start a new VM
    subprocess.run(['vmrun', 'clone', path, vmname])
    subprocess.run(['vmrun', 'start', vmname])
    print(f"Deploying a VM from {path} with name {vmname}")

def deploy_remote(host, user, pwd):
    # Connect to vCenter
    si = SmartConnect(host=host, user=user, pwd=pwd)
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()
    root_folder = content.rootFolder
    resource_pool = root_folder.childEntity[0].resourcePool
    datastore = root_folder.childEntity[0].datastore[0]
    # Create a new vm config spec
    vm_config = vim.vm.ConfigSpec(
        name='new_vm',
        memoryMB=2048,
        numCPUs=2,
        files=vim.vm.FileInfo(logDirectory=None,
                               snapshotDirectory=None,
                               suspendDirectory=None,
                               vmPathName="[" + datastore.name + "] new_vm"),
        deviceChange=[
            vim.vm.device.VirtualDeviceSpec(
                operation='add',
                device=vim.vm.device.VirtualE1000(
                    key=-1,
                    deviceInfo=vim.Description(
                        label='Network Adapter 1',
                        summary='VM Network'
                    )
                )
            )
        ]
    )
    # Create & power on the new VM
    root_folder.CreateVm(config=vm_config, pool=resource_pool)
    new_vm = root_folder.childEntity[0].vm[0]
    new_vm.PowerOn()
    print("New virtual machine '{}' has been deployed and powered on.".format(new_vm.name))
    si.logout()

def main():
    parser = argparse.ArgumentParser(description='Deploy a VM')
    parser.add_argument('--local', action='store_true', help='Deploy a VM locally')
    parser.add_argument('--remote', action='store_true', help='Deploy a VM remotely')
    parser.add_argument('--path', type=str, help='Path to the VM image')
    parser.add_argument('--vmname', type=str, help='Name of the new VM') 
    parser.add_argument('--host', type=str, help='Vcenter hostname')
    parser.add_argument('--user', type=str, help='Username')
    parser.add_argument('--pwd', type=str, help='Password')
    args = parser.parse_args()
    if args.local and args.remote:
        print("Please select only one option")
    if args.local:
        deploy_local(args.path, args.vmname)
    elif args.remote:
        deploy_remote(args.host, args.user, args.pwd)
    if args.local and (args.path is None or args.vmname is None):
        parser.error("--local option requires --path and --vmname options")
    elif args.remote and (args.host is None or args.user is None or args.pwd is None):
        parser.error("--remote option requires --host, --user, and --pwd options")
    else:
        print("Use -h to see the options")

if __name__=="__main__": 
	main()
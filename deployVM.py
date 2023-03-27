import argparse
import subprocess
from typing import Optional

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import atexit


def deploy_local(path: str, vmname: str) -> None:
    subprocess.run(['vmrun', 'clone', path, vmname])
    subprocess.run(['vmrun', 'start', vmname])
    print(f"Deploying a VM from {path} with name {vmname}")


def deploy_remote(host: str, user: str, pwd: str) -> None:
    si = SmartConnect(host=host, user=user, pwd=pwd)
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()
    root_folder = content.rootFolder
    resource_pool = root_folder.childEntity[0].resourcePool
    datastore = root_folder.childEntity[0].datastore[0]

    vm_config = create_vm_config_spec(datastore)

    root_folder.CreateVm(config=vm_config, pool=resource_pool)
    new_vm = root_folder.childEntity[0].vm[0]
    new_vm.PowerOn()
    print(f"New virtual machine '{new_vm.name}' has been deployed and powered on.")
    si.logout()


def create_vm_config_spec(datastore: vim.Datastore) -> vim.vm.ConfigSpec:
    return vim.vm.ConfigSpec(
        name='new_vm',
        memoryMB=2048,
        numCPUs=2,
        files=vim.vm.FileInfo(logDirectory=None,
                               snapshotDirectory=None,
                               suspendDirectory=None,
                               vmPathName=f"[{datastore.name}] new_vm"),
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


def main() -> None:
    parser = argparse.ArgumentParser(description='Deploy a VM')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--local', action='store_true', help='Deploy a VM locally')
    group.add_argument('--remote', action='store_true', help='Deploy a VM remotely')
    parser.add_argument('--path', type=str, help='Path to the VM image')
    parser.add_argument('--vmname', type=str, help='Name of the new VM')
    parser.add_argument('--host', type=str, help='Vcenter hostname')
    parser.add_argument('--user', type=str, help='Username')
    parser.add_argument('--pwd', type=str, help='Password')
    args = parser.parse_args()

    if args.local:
        if args.path is None or args.vmname is None:
            parser.error("--local option requires --path and --vmname options")
        deploy_local(args.path, args.vmname)
    elif args.remote:
        if args.host is None or args.user is None or args.pwd is None:
            parser.error("--remote option requires --host, --user, and --pwd options")
        deploy_remote(args.host, args.user, args.pwd)


if __name__ == "__main__":
    main()

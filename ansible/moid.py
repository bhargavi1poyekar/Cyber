from pyvmomi.connect import SmartConnect, Disconnect
import ssl

# Disable SSL certificate verification (not recommended for production use)
ssl._create_default_https_context = ssl._create_default_https_context_disabled

# vCenter Server connection details
vcenter_host = 'vcenter1.umbc.edu'
vcenter_user = 'crange1'
vcenter_password = 'Crcsee2#'

# IP address of the VM you want to find
vm_ip_address = '130.85.121.26'

def find_vm_by_ip_address(vm_ip_address):
    try:
        # Connect to vCenter Server
        service_instance = SmartConnect(
            host=vcenter_host,
            user=vcenter_user,
            pwd=vcenter_password
        )

        # Search for the virtual machine by IP address
        content = service_instance.RetrieveContent()
        container = content.rootFolder
        view_type = [vim.VirtualMachine]
        recursive = True
        container_view = content.viewManager.CreateContainerView(container, view_type, recursive)
        vm_list = container_view.view
        vm_moid = None
        vm_name = None

        for vm in vm_list:
            if vm.guest.ipAddress == vm_ip_address:
                vm_moid = vm._moId
                vm_name = vm.name
                break

        # Disconnect from vCenter Server
        Disconnect(service_instance)

        return vm_moid, vm_name

    except Exception as e:
        print(f"Error: {e}")
        return None, None

# Find the MOID and name of the VM by its IP address
vm_moid, vm_name = find_vm_by_ip_address(vm_ip_address)
if vm_moid and vm_name:
    print(f"The MOID of VM '{vm_name}' with IP address '{vm_ip_address}' is: {vm_moid}")
else:
    print(f"VM with IP address '{vm_ip_address}' not found.")

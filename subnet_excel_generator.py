import ipaddress


def calculate_prefix_length(hosts_per_subnet):
    """
    Calculate the CIDR prefix length needed to support
    the requested number of usable hosts.
    """
    if not isinstance(hosts_per_subnet, int) or isinstance(hosts_per_subnet, bool) or hosts_per_subnet <= 0:
        raise ValueError("Hosts per subnet must be a positive integer.")
    required_addresses = hosts_per_subnet + 2
    host_bits = (required_addresses - 1).bit_length()
    prefix_length = 32 - host_bits

    if prefix_length < 0:
        raise ValueError("Host requirement is too large for IPv4.")

    return prefix_length, host_bits


def get_usable_host_range(network):
    """
    Calculate the first and last usable host in a subnet
    without generating a full list of all hosts.
    """
    if network.prefixlen == 32:
        return network.network_address, network.network_address

    if network.prefixlen == 31:
        return network.network_address, network.broadcast_address

    first_host = ipaddress.ip_address(int(network.network_address) + 1)
    last_host = ipaddress.ip_address(int(network.broadcast_address) - 1)

    return first_host, last_host


def calculate_subnets(starting_ip, num_subnets, hosts_per_subnet):
    """
    Generate subnet information based on the starting IP,
    number of subnets, and required usable hosts per subnet.
    """
    if not isinstance(num_subnets, int) or isinstance(num_subnets, bool) or not 1 <= num_subnets <= 100000:
        raise ValueError("Number of subnets must be between 1 and 100000.")
    prefix_length, host_bits = calculate_prefix_length(hosts_per_subnet)

    current_network = ipaddress.IPv4Network(
        f"{starting_ip}/{prefix_length}",
        strict=False
    )

    if int(current_network.network_address) + num_subnets * current_network.num_addresses > 2 ** 32:
        raise ValueError("Requested subnets extend beyond the IPv4 address space.")

    subnet_data = []

    for subnet_number in range(1, num_subnets + 1):
        first_host, last_host = get_usable_host_range(current_network)

        subnet_data.append({
            "Subnet Number": subnet_number,
            "Network Address": str(current_network.network_address),
            "First Usable Host": str(first_host),
            "Last Usable Host": str(last_host),
            "Broadcast Address": str(current_network.broadcast_address),
            "Subnet Mask": str(current_network.netmask),
            "CIDR": f"/{prefix_length}",
            "Total Addresses": current_network.num_addresses,
            "Usable Hosts": max(current_network.num_addresses - 2, 1)
        })

        if subnet_number < num_subnets:
            next_network_address = int(current_network.network_address) + current_network.num_addresses
            current_network = ipaddress.IPv4Network((next_network_address, prefix_length))

    return subnet_data, host_bits


def main():
    print("Subnet Excel Generator")
    print("This tool calculates subnets and exports the results to Excel.")
    print()

    try:
        starting_ip = input("Enter the starting IP address, example 192.168.1.0: ").strip()
        num_subnets = int(input("How many subnets do you need? "))
        hosts_per_subnet = int(input("How many usable hosts per subnet? "))

        if num_subnets <= 0:
            raise ValueError("Number of subnets must be greater than zero.")

        if hosts_per_subnet <= 0:
            raise ValueError("Hosts per subnet must be greater than zero.")

        subnet_data, host_bits = calculate_subnets(
            starting_ip,
            num_subnets,
            hosts_per_subnet
        )

        import pandas as pd

        df = pd.DataFrame(subnet_data)

        from pathlib import Path
        output_file = "subnet_calculations.xlsx"
        if Path(output_file).exists():
            if input(f"{output_file} exists. Overwrite? (y/N): ").strip().lower() != "y":
                print("Export cancelled.")
                return
        df.to_excel(output_file, index=False)

        print()
        print("=" * 50)
        print("Calculation complete.")
        print(f"Each subnet uses {host_bits} host bits.")
        print(f"Excel file created: {output_file}")
        print("=" * 50)

    except ValueError as error:
        print(f"Input error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
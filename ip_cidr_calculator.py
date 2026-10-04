def main():
    # IP Address and CIDR Notation Processor
    print("Enter IP/CIDR (example: 192.168.1.10/24)")
    ip_cidr = input("Enter IP/CIDR here: ").strip()

    while "/" not in ip_cidr:
        print("IP/CIDR must be in the form of x.x.x.x/x")
        ip_cidr = input("Enter IP/CIDR here: ").strip()

    ip_part, cidr_part = ip_cidr.split("/", 1)
    octets = ip_part.split(".")

    if not (cidr_part.isascii() and cidr_part.isdigit()) or int(cidr_part) < 0 or int(cidr_part) > 32:
        print("INVALID CIDR. Must be a number 0-32.")
        return

    if len(octets) != 4:
        print("INVALID IP ADDRESS FORMAT")
        return

    for abc in octets:
        if not (abc.isascii() and abc.isdigit()):
            print("INVALID IP. Octets must be numbers.")
            return
        num = int(abc)
        if num < 0 or num > 255:
            print("INVALID IP. Each octet must be 0-255.")
            return

    # Convert CIDR to subnet mask
    mask_bits = "1" * int(cidr_part) + "0" * (32 - int(cidr_part))
    m1 = int(mask_bits[0:8], 2)
    m2 = int(mask_bits[8:16], 2)
    m3 = int(mask_bits[16:24], 2)
    m4 = int(mask_bits[24:32], 2)
    subnet_mask = f"{m1}.{m2}.{m3}.{m4}"

    mask_parts = [int(x) for x in subnet_mask.split(".")]
    wildcard_parts = [255 - mask for mask in mask_parts]
    wildcard_mask = ".".join(str(x) for x in wildcard_parts)

    # Octet containing the block increment (whole-octet boundaries included).
    prefix = int(cidr_part)
    subnet_octet_index = min(prefix // 8, 3)
    block_size = 1 if prefix == 32 else 2 ** (8 - prefix % 8)

    # Calculate network address
    ip_nums = [int(abc) for abc in octets]
    network_address = [ip_nums[i] & mask_parts[i] for i in range(4)]
    network_address_str = ".".join(str(x) for x in network_address)

    # Calculate broadcast address
    broadcast_address = [network_address[i] | (255 - mask_parts[i]) for i in range(4)]
    broadcast_address_str = ".".join(str(x) for x in broadcast_address)

    # Calculate usable host range and host counts
    total_addresses = 2 ** (32 - int(cidr_part))
    host_bits = 32 - int(cidr_part)

    if int(cidr_part) == 32:
        usable_hosts = 1
    elif int(cidr_part) == 31:
        usable_hosts = 2
    else:
        usable_hosts = total_addresses - 2

    if int(cidr_part) >= 31:
        first_usable = network_address[:]
        last_usable = broadcast_address[:]
    else:
        first_usable = network_address[:]
        first_usable[3] += 1
        last_usable = broadcast_address[:]
        last_usable[3] -= 1

    first_usable_str = ".".join(str(x) for x in first_usable)
    last_usable_str = ".".join(str(x) for x in last_usable)

    reserved_addresses = 0 if int(cidr_part) > 30 else 2
    network_bits = int(cidr_part)

    print("----------------------- Identity / Scope ------------------------------")
    print(f"Network address: {network_address_str}")
    print(f"Broadcast address: {broadcast_address_str}")

    print("----------------------- Masking details -------------------------------")
    print(f"Subnet mask: {subnet_mask}")
    print(f"Wildcard mask: {wildcard_mask}")
    print(f"Network bits: {network_bits}")
    print(f"Host bits: {host_bits}")
    print(f"Subnetting octet: {subnet_octet_index + 1}")
    print(f"Block size: {block_size}")

    print("-------------------------- Capacity -----------------------------------")
    print(f"Total addresses: {total_addresses}")
    print(f"Usable hosts: {usable_hosts}")
    print(f"Reserved addresses: {reserved_addresses}")

    print("--------------------------- Usability ---------------------------------")
    print(f"First usable IP: {first_usable_str}")
    print(f"Last usable IP: {last_usable_str}")


if __name__ == "__main__":
    main()

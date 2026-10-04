# IPv4 Subnet Tools

A manual IPv4/CIDR calculator and a subnet planner that exports an Excel workbook.
The first tool demonstrates bitwise network and broadcast calculations; the second
uses Python's `ipaddress` library to plan consecutive, equally sized networks.

## Run the calculator

Use Python 3.12 or newer. The calculator needs no third-party packages.

```sh
python ip_cidr_calculator.py
```

Enter `192.168.1.10/24`. Expected results include network `192.168.1.0`,
broadcast `192.168.1.255`, mask `255.255.255.0`, and 254 usable hosts.
The calculator treats /31 as two usable addresses and /32 as one.
"Subnetting octet" means the octet containing the block increment: for /24,
this is octet 4 with block size 256; for /32 it is octet 4 with block size 1.

## Run the Excel planner

```sh
python -m pip install -r requirements.txt
python subnet_excel_generator.py
```

Example answers: `192.168.1.0`, `4`, `50`.
The four networks are `192.168.1.0/26`, `192.168.1.64/26`,
`192.168.1.128/26`, and `192.168.1.192/26`, each with 62 usable hosts.
The workbook `subnet_calculations.xlsx` is written to the current directory.
An existing workbook requires an explicit overwrite answer.

The starting address is rounded down to its network boundary. This planner reserves
network and broadcast addresses, so requests for one or two hosts use /30;
it does not plan /31 point-to-point links. Inputs must be IPv4. Requests extending
past 255.255.255.255 are rejected. The interactive planner caps output at 100,000
subnets to limit memory and workbook size. It does not scan a network.

## Test

```sh
python -m unittest -v
```

Core tests use only the standard library. Excel export was separately exercised
with pandas 3.0.1 and openpyxl 3.1.5 on Python 3.12.14. The requirements list is
intentionally unpinned; it is not a reproducible dependency lockfile.

## Project history

See [CHANGES.md](CHANGES.md) for the preparation notes.

No distribution license has been selected for this project.

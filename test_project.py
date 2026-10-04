import contextlib
import io
import ipaddress
import unittest
from unittest.mock import patch
from ip_cidr_calculator import main
from subnet_excel_generator import calculate_subnets, calculate_prefix_length

class SubnetTests(unittest.TestCase):
    def cli(self, value):
        out = io.StringIO()
        with patch('builtins.input', return_value=value), contextlib.redirect_stdout(out):
            main()
        return out.getvalue()

    def test_every_prefix_against_standard_library(self):
        for prefix in range(33):
            for address in ('0.0.0.0', '192.168.1.10', '255.255.255.255'):
                with self.subTest(prefix=prefix, address=address):
                    network = ipaddress.IPv4Network(f'{address}/{prefix}', strict=False)
                    out = self.cli(f'{address}/{prefix}')
                    first = network.network_address if prefix >= 31 else network.network_address + 1
                    last = network.broadcast_address if prefix >= 31 else network.broadcast_address - 1
                    hosts = network.num_addresses if prefix >= 31 else network.num_addresses - 2
                    for line in (f'Network address: {network.network_address}',
                                 f'Broadcast address: {network.broadcast_address}',
                                 f'Subnet mask: {network.netmask}',
                                 f'First usable IP: {first}', f'Last usable IP: {last}',
                                 f'Usable hosts: {hosts}'):
                        self.assertIn(line + '\n', out)

    def test_block_boundaries(self):
        for prefix, octet, block in [(0,1,256),(8,2,256),(16,3,256),(24,4,256),(25,4,128),(32,4,1)]:
            out = self.cli(f'192.168.1.10/{prefix}')
            self.assertIn(f'Subnetting octet: {octet}\n', out)
            self.assertIn(f'Block size: {block}\n', out)

    def test_invalid_cli_input(self):
        for value in ('1.2.3.999/24', '1.2.3.4/33', 'a.b.c.d/24', '1.2.3.4/²'):
            self.assertIn('INVALID', self.cli(value))

    def test_four_subnets(self):
        rows, bits = calculate_subnets('192.168.1.10', 4, 50)
        self.assertEqual(bits, 6)
        self.assertEqual([r['Network Address'] for r in rows], ['192.168.1.0','192.168.1.64','192.168.1.128','192.168.1.192'])
        self.assertEqual(rows[-1]['Last Usable Host'], '192.168.1.254')

    def test_last_ipv4_subnet_and_full_space(self):
        rows, _ = calculate_subnets('255.255.255.252', 1, 2)
        self.assertEqual(rows[0]['Broadcast Address'], '255.255.255.255')
        rows, _ = calculate_subnets('0.0.0.0', 1, 2**32-2)
        self.assertEqual(rows[0]['CIDR'], '/0')

    def test_invalid_requests(self):
        for args in [('::1',1,2),('255.255.255.252',2,2),('1.2.3.4',0,2),('1.2.3.4',100001,2),('1.2.3.4',1,0),('1.2.3.4',1,2**32)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                calculate_subnets(*args)
        self.assertEqual(calculate_prefix_length(1), (30, 2))

if __name__ == '__main__':
    unittest.main()

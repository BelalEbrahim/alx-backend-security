from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP
import ipaddress


class Command(BaseCommand):
    help = "Add one or more IP addresses or IP ranges to the BlockedIP blacklist."

    def add_arguments(self, parser):
        parser.add_argument(
            "ips",
            nargs="+",
            help="IP address(es) or IP range(s) to block (IPv4 or IPv6, e.g., 192.168.1.1 or 192.168.1.0/24).",
        )
        parser.add_argument(
            "--reason",
            default="Manually blocked via command",
            help="Reason for blocking the IP(s).",
        )

    def handle(self, *args, **options):
        reason = options["reason"]

        for ip_input in options["ips"]:
            try:
                # Check if input is a single IP or a network range
                try:
                    ip = ipaddress.ip_address(ip_input)
                    ip_list = [ip]
                except ValueError:
                    # Try parsing as a network range
                    network = ipaddress.ip_network(ip_input, strict=False)
                    ip_list = list(network)

                for ip in ip_list:
                    ip_str = str(ip)
                    # Check if IP already exists
                    if BlockedIP.objects.filter(ip_address=ip_str).exists():
                        self.stdout.write(f"{ip_str} is already blocked")
                        continue

                    # Create new BlockedIP entry
                    BlockedIP.objects.create(
                        ip_address=ip_str,
                        reason=reason
                    )
                    self.stdout.write(self.style.SUCCESS(f"Blocked {ip_str} (Reason: {reason})"))

            except ValueError as e:
                self.stderr.write(self.style.ERROR(f"Invalid IP or range: {ip_input} ({str(e)})"))
                continue

from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP
import ipaddress


class Command(BaseCommand):
    help = "Add one or more IP addresses to the BlockedIP blacklist."

    def add_arguments(self, parser):
        parser.add_argument(
            "ips",
            nargs="+",
            help="IP address(es) to block (IPv4 or IPv6).",
        )

    def handle(self, *args, **options):
        for ip in options["ips"]:
            try:
                # Validate IP
                ipaddress.ip_address(ip)
            except ValueError:
                self.stderr.write(self.style.ERROR(
                    f"Invalid IP address: {ip}"))
                continue

            _, created = BlockedIP.objects.get_or_create(ip_address=ip)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Blocked {ip}"))
            else:
                self.stdout.write(f"{ip} is already blocked")

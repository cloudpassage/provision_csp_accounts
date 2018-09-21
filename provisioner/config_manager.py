"""All runtime configuration is handled here."""
import argparse


class ConfigManager(object):
    """Manage runtime configuration for bulk_provision_aws_accounts.py.

    All configuration values are derived from command-line arguments.

    Variables:
        halo_api_key (str): API key ID for Halo access.
        halo_api_secret_key (str): API key secret.
        csv_file_location (str): Path to CSV file.
        external_id (str): External ID to be configured for all CSP accounts
            configured by this tool.
        account_id_column (str): Column in CSV file which contains the AWS
            account ID.
        account_display_name_column (str): Column in CSV file which contains
            the display name for the AWS account.
        target_halo_group_id (str): ID for group in halo where CSP accounts
            will be provisioned.
        role_name (str): Name of role in AWS, which Halo will assume for
            auditing the CSP account.
    """

    def __init__(self):
        return

    def set_config_from_args(self):
        desc = 'Bulk-provision AWS accounts in Halo'
        args = [('halo_api_key', 'Halo API key'),
                ('halo_api_secret_key', 'Halo API secret'),
                ('csv_file_location', 'Path to CSV file'),
                ('external_id', 'External ID for AWS role assumption'),
                ('account_id_column', 'CSV column containing AWS account ID'),
                ('account_display_name_column', 'CSV column for account desc'),
                ('target_halo_group_id',
                 'ID of Halo group for provisioning CSP accounts'),
                ('role_name',
                 'Name of role to be used for auditing AWS accounts.')]
        parser = argparse.ArgumentParser(description=desc)
        for arg in args:
            parser.add_argument(arg[0], help=arg[1])
        parser.add_argument('--dry_run', action="store_true",
                            help="Dry run. Do not make changes.")
        parser.parse_args(namespace=self)

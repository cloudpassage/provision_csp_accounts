# provision_csp_accounts

[![Build Status](https://travis-ci.com/cloudpassage/provision_csp_accounts.svg?branch=master)](https://travis-ci.com/cloudpassage/provision_csp_accounts)
[![Maintainability](https://api.codeclimate.com/v1/badges/681a5a187498df3a098e/maintainability)](https://codeclimate.com/github/cloudpassage/provision_csp_accounts/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/681a5a187498df3a098e/test_coverage)](https://codeclimate.com/github/cloudpassage/provision_csp_accounts/test_coverage)

## What is this?

This is a tool for provisioning AWS accounts in the CloudPassage Halo platform.

## How does it work?

When the user runs the tool, the tool consumes a CSV file of AWS accounts, and
compares the CSV file against what's provisioned in the user's Halo account.
The accounts which are not already provisioned in Halo will be provisioned.
Accounts which are already provisioned in Halo but do not have matching
`account_display_name` configured, will have the `account_display_name` field
updated.

## What are the requirements?

This tool is tested to be compatible with Python 2.7.12.

Requirements are listed in `requirements.txt`. For convenience, you may install
these requirements with `python2.7 -m pip install -r requirements.txt` from the
base directory of this repository.

## How do I use the tool?

IMPORTANT: This tool assumes that you already have roles configured in all
accounts described in your CSV file. This tool will error out if it
encounters an ARN/ExternalID pair that don't work. So provision the roles
required for Halo to monitor your accounts _before_ you run this tool.

usage:
`provision_aws_accounts.py [-h] [--dry_run] halo_api_key
halo_api_secret_key csv_file_location external_id account_id_column
account_display_name_column target_halo_group_id role_name`

Bulk-provision AWS accounts in Halo

```
positional arguments:
  halo_api_key                Halo API key
  halo_api_secret_key         Halo API secret
  csv_file_location           Path to CSV file
  external_id                 External ID for AWS role assumption
  account_id_column           CSV column containing AWS account ID
  account_display_name_column CSV column for account display name
  target_halo_group_id        ID of Halo group for provisioning CSP accounts
  role_name                   Name of role to be used for auditing AWS accounts.

optional arguments:
  -h, --help            show this help message and exit
  --dry_run             Dry run. Do not make changes.
```

## Error messages?

Meaningful error messages will be thrown for the following conditions:
* Bad Halo API credentials.
* Halo API key does not have sufficient privileges to provision accounts.
* CSV file does not exist.
* Columns for account ID and account display name do not exist in CSV.
* ARN and external ID are invalid.

<!---
#CPTAGS:community-supported automation
#TBICON:images/python_icon.png
-->

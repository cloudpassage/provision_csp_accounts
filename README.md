# provision_csp_accounts

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

## How do I run the tool?

## Error messages?

Meaningful error messages will be thrown for the following conditions:
* Bad Halo API credentials.
* Halo API key does not have sufficient privileges to provision accounts.
* CSV file does not exist.
* Columns for account ID and account display name do not exist in CSV.

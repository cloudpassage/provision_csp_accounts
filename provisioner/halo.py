"""Halo interaction happens here."""
import cloudpassage
import re
import sys


class Halo(object):
    """Interact with the CloudPassage Halo API.

    Args:
        config (object): Instance of provisioner.ConfigManager()
    """
    def __init__(self, config):
        self.halo_api_key = config.halo_api_key
        self.halo_api_secret_key = config.halo_api_secret_key
        self.session = cloudpassage.HaloSession(self.halo_api_key,
                                                self.halo_api_secret_key)
        return

    @classmethod
    def construct_role_arn(self, account_id, role_name):
        """Return AWS role ARN, constructed from account_id and role_name."""
        role_arn = "arn:aws:iam::%s:role/%s" % (account_id, role_name)
        return role_arn

    def get_all_csp_accounts(self):
        """Return a list of all CSP accounts."""
        http_helper = cloudpassage.HttpHelper(self.session)
        accounts = http_helper.get_paginated("/v1/csp_accounts",
                                             "csp_accounts", 99)
        return accounts

    def provision_csp_account(self, account_id, display_name, role_name,
                              external_id, group_id, csp_account_type="AWS"):
        """Provision a CSP account in Halo.

        Args:
            account_id (str): Account ID to be used in provisioning.
            display_name (str): Account display name.
            role_name (str): Used with account_id to construct role ARN.
            external_id (str): External ID required for assuming role in AWS
                account.
            csp_account_type (str): Cloud provider. Only `aws` is currently
                supported.

        Returns:
            str: Halo ID for CSP account
        """
        http_helper = cloudpassage.HttpHelper(self.session)
        payload = {"external_id": external_id,
                   "role_arn": self.construct_role_arn(account_id, role_name),
                   "group_id": group_id,
                   "csp_account_type": csp_account_type}
        try:
            halo_csp_account_id = http_helper.post("/v1/csp_accounts", payload)
        except cloudpassage.CloudPassageAuthorization as e:
            print("Failed to provision account. Not authorized!\n%s" % e)
            sys.exit(1)
        except cloudpassage.CloudPassageValidation as e:
            print("Validation failure when creating account: %s" % e)
            print("ARN and external ID will fail if they don't exist.")
            sys.exit(1)
        return halo_csp_account_id

    def sanity_check(self):
        """Perform a pre-flight sanity check, exit if authentication fails."""
        try:
            self.session.authenticate_client()
        except cloudpassage.CloudPassageAuthentication:
            msg = """Failed to authenticate to the CloudPassage Halo API.
                  \nPlease check your API key and secret, and try again."""
            print(msg)
            sys.exit(1)

    def update_csp_display_name(self, halo_csp_account_id, display_name):
        """Update account_display_name for CSP account in Halo.

        Args:
            halo_csp_account_id (str): ID for Halo CSP account object. This is
                NOT the CSP account ID.
            display_name (str): String to be substituted for existing
                `account_display_name` for CSP account in Halo.

        Returns:
            None
        """
        # Guard against URL traversal, etc...
        try:
            self.validate_object_id(halo_csp_account_id)
        except cloudpassage.CloudPassageValidation as e:
            print("Halo CSP ID failed validation!: %s" % e)
            sys.exit(1)
        http_helper = cloudpassage.HttpHelper(self.session)
        url = "/v1/csp_accounts/%s" % halo_csp_account_id
        payload = {"account_display_name": display_name}
        http_helper.put(url, payload)
        return

    @classmethod
    def validate_object_id(cls, object_id):
        """Validates object ID (server_id, policy_id, etc...)

        This function validates Object IDs with the intent of guarding against
        URL traversal.

        Args:
            object_id (str or list): Object ID to be validated

        Returns:
            None

        Raises:
            CloudPassageValidation if validation fails.
        """
        rex = re.compile('^[A-Za-z0-9-]+$')
        if isinstance(object_id, (basestring)):
            if not rex.match(object_id):
                message = "Object ID failed validation: %s" % object_id
                raise cloudpassage.CloudPassageValidation(message)
            else:
                return True
        elif isinstance(object_id, list):
            for individual in object_id:
                cls.validate_object_id(individual)
            return True
        else:
            message = "Wrong type for objectID:%s" % str(type(object_id))
            raise cloudpassage.CloudPassageValidation(message)

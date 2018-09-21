"""This blends data."""


class Blender(object):
    """Parse and compare data from Halo and CSV.

    Args:
        halo_data (list): List of dictionary objects, where dictionary objects
            are from Halo API, /v1/csp_accounts.
        csv_tups (list): List of tuples from CSV, where position 0 contains
            account ID and position 1 contains account display name.
    """
    def __init__(self, halo_data, csv_tups):
        self.halo_data = halo_data
        self.csv_tups = csv_tups

    def create_change_set(self):
        change_set = {"create": [],
                      "update": []}
        for row in self.csv_tups:
            # If we aren't monitoring account...
            if not self.account_is_monitored(row):
                change_set["create"].append(row)
                continue
            # If we are monitoring but account_display_name is wrong...
            match = self.account_display_name_needs_updating(row)
            if match:
                change_set["update"].append((match, row[1]))
        return change_set

    def account_is_monitored(self, row):
        """Return True if CSP account is already monitored in Halo.

        Args:
            row (tup): Tuple containing account_id in pos 0 and accouount
                display name in pos 1.

        Returns:
            bool: True if account is in self.halo_data
        """
        if [x for x in self.halo_data if x["csp_account_id"] == row[0]]:
            return True
        else:
            return False

    def account_display_name_needs_updating(self, row):
        """Return Halo CSP account ID if account display name does not match.

        Args:
            row (tup): Tuple containing account_id in pos 0 and accouount
                display name in pos 1.

        Returns:
            str: Halo CSP account ID if account display name needs updating,
                else None.
        """
        match = [x["id"] for x in self.halo_data
                 if x["csp_account_id"] == row[0]
                 and x["account_display_name"] != row[1]]
        if match:
            return match[0]
        else:
            return None

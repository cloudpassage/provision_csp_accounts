"""CSV consumer"""
import csv
import os
import sys


class CsvConsumer(object):
    """Consume and process information from CSV file.

    Args:
        config (object): Instance of provisioner.ConfigManager class.

    Variables:
        csv_file_location (str): Path to CSV file.
        account_id_column (str): Column containing account ID.
        account_display_name_column (str): Column containing account display
            name.
    """

    def __init__(self, config):
        self.csv_file_location = config.csv_file_location
        self.account_id_column = config.account_id_column
        self.account_display_name_column = config.account_display_name_column
        self.sanity_check()
        return

    def get_account_metadata(self):
        """Return a list of tuples derived from CSV.

        A list of tuples is returned, where position 0 holds the account ID,
        and position 1 holds the account display name.
        """
        rows = self.get_rows()
        id_col = self.account_id_column
        disp_name = self.account_display_name_column
        result = [(r[id_col], r[disp_name]) for r in rows]
        return result

    def get_columns(self):
        """Return a list of column headers from a CSV file."""
        with open(self.csv_file_location, 'rU') as csv_file:
            reader = csv.DictReader(csv_file)
            columns = reader.fieldnames
        return columns

    def get_rows(self):
        """Returna list of dictionary objects representing rows of the CSV."""
        with open(self.csv_file_location, 'rU') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = [row for row in reader]
        return rows

    def sanity_check(self):
        """Check config for sanity."""
        sanity = True
        if not os.path.isfile(self.csv_file_location):
            print("CSV file does not exist: %s" % self.csv_file_location)
            sys.exit(1)
        csv_columns = self.get_columns()
        for col in [(self.account_id_column, "account_id_column"),
                    (self.account_display_name_column,
                     "account_display_name_column")]:
            if col[0] not in csv_columns:
                sanity = False
                print("Misconfigured variable %s: %s (column does not exist)" %
                      (col[1], col[0]))
        if sanity is False:
            sys.exit(1)

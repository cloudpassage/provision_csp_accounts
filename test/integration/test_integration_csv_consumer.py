import provisioner
import pytest
import os

here_dir = os.path.abspath(os.path.dirname(__file__))
fixture_dir = os.path.join(here_dir, "../fixture")


class TestIntegrationCsvConsumer(object):
    def good_config_wincr(self):
        """Return a dummy config object for CsvConsumer.
        CSV contains Windows-style newlines.
        """
        config = provisioner.ConfigManager()
        config.csv_file_location = os.path.join(fixture_dir, "win_accts.csv")
        config.account_id_column = "Account ID"
        config.account_display_name_column = "Account Name"
        return config

    def good_config_lincr(self):
        """Return a dummy config object for CsvConsumer.
        CSV contains Linux-style newlines.
        """
        config = provisioner.ConfigManager()
        config.csv_file_location = os.path.join(fixture_dir, "lin_accts.csv")
        config.account_id_column = "Account ID"
        config.account_display_name_column = "Account Name"
        return config

    def bad_col_config(self):
        """Return a dummy config object with bad column references."""
        config = provisioner.ConfigManager()
        config.csv_file_location = os.path.join(fixture_dir, "lin_accts.csv")
        config.account_id_column = "noname"
        config.account_display_name_column = "noname"
        return config

    def bad_file_config(self):
        """Return a dummy config object with bad file reference."""
        config = provisioner.ConfigManager()
        config.csv_file_location = os.path.join(fixture_dir, "nonexistent.csv")
        config.account_id_column = "Account ID"
        config.account_display_name_column = "Account Name"
        return config

    def create_csv_consumer(self, config):
        """Return a CsvConsumer object."""
        return provisioner.CsvConsumer(config)

    def test_instantiate_csv_consumer(self):
        """Test instantiation of CsvConsumer()."""
        assert self.create_csv_consumer(self.good_config_wincr())

    def test_bad_column_reference(self):
        """Assert clean exit from bad column name config."""
        with pytest.raises(SystemExit) as e:
            self.create_csv_consumer(self.bad_col_config())
        assert e.type == SystemExit
        assert e.value.code == 1

    def test_bad_file_reference(self):
        """Assert clean exit from invalid file name config."""
        with pytest.raises(SystemExit) as e:
            self.create_csv_consumer(self.bad_file_config())
        assert e.type == SystemExit
        assert e.value.code == 1

    def test_get_rows_from_win_file(self):
        """Assert that we get 10 rows from the Windows CSV file."""
        csv_consumer = self.create_csv_consumer(self.good_config_wincr())
        rows_as_dict = csv_consumer.get_rows()
        assert len(rows_as_dict) == 6

    def test_get_account_win_metadata(self):
        """Assert that we get complete tuples from Windows CSV file."""
        csv_consumer = self.create_csv_consumer(self.good_config_wincr())
        tups = csv_consumer.get_account_metadata()
        for t in tups:
            assert t[0] != ""
            assert t[1] != ""

    def test_get_rows_from_lin_file(self):
        """Assert that we get 10 rows from the Linux CSV file."""
        csv_consumer = self.create_csv_consumer(self.good_config_lincr())
        rows_as_dict = csv_consumer.get_rows()
        assert len(rows_as_dict) == 6

    def test_get_account_lin_metadata(self):
        """Assert that we get complete tuples from Linux CSV file."""
        csv_consumer = self.create_csv_consumer(self.good_config_lincr())
        tups = csv_consumer.get_account_metadata()
        for t in tups:
            assert t[0] != ""
            assert t[1] != ""

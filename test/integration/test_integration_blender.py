import json
import provisioner
import os

here_dir = os.path.abspath(os.path.dirname(__file__))
fixture_dir = os.path.join(here_dir, "../fixture")


class TestIntegrationBlender(object):
    def good_config_wincr(self):
        """Return a dummy config object for CsvConsumer.
        CSV contains Windows-style newlines.
        """
        config = provisioner.ConfigManager()
        config.csv_file_location = os.path.join(fixture_dir, "win_accts.csv")
        config.account_id_column = "Account ID"
        config.account_display_name_column = "Account Name"
        return config

    def get_halo_account_data(self):
        """Get fake Halo API data."""
        json_file_path = os.path.join(fixture_dir, "halo_accounts.json")
        with open(json_file_path, 'r') as json_file:
            halo_accounts = json.load(json_file)
        return halo_accounts

    def get_csv_update_data(self):
        """Get data to be updated from CSV file."""
        config = self.good_config_wincr()
        csv_consumer = provisioner.CsvConsumer(config)
        return csv_consumer.get_account_metadata()

    def test_get_change_set(self):
        """Test change set from blending CSV and existing Halo account info."""
        update_tup = ("920b3f30-9204-469a-967c-878aa4a77c07", "oneword")
        create_tup = ("123123000000", "AccountNameCamelCase")
        halo_data = self.get_halo_account_data()
        csv_data = self.get_csv_update_data()
        blender = provisioner.Blender(halo_data, csv_data)
        change_set = blender.create_change_set()
        assert "create" in change_set.keys()
        assert "update" in change_set.keys()
        assert update_tup in change_set["update"]
        assert create_tup in change_set["create"]
        assert isinstance(change_set["update"][0][0], basestring)
        assert isinstance(change_set["update"][0][1], basestring)
        assert isinstance(change_set["create"][0][0], basestring)
        assert isinstance(change_set["create"][0][1], basestring)
        assert len(change_set["create"]) == 4
        assert len(change_set["update"]) == 1

    def test_account_is_monitored_false(self):
        row = ('abc123', 'unmonitored_account')
        halo_data = self.get_halo_account_data()
        csv_data = self.get_csv_update_data()
        blender = provisioner.Blender(halo_data, csv_data)
        result = blender.account_is_monitored(row)
        assert result is False

    def test_account_is_monitored_true(self):
        row = ('357886268579', 'agseteam1')
        halo_data = self.get_halo_account_data()
        csv_data = self.get_csv_update_data()
        blender = provisioner.Blender(halo_data, csv_data)
        result = blender.account_is_monitored(row)
        assert result is True

    def test_account_display_name_needs_updating_false(self):
        row = ('357886268579', 'agseteam1')
        halo_data = self.get_halo_account_data()
        csv_data = self.get_csv_update_data()
        blender = provisioner.Blender(halo_data, csv_data)
        result = blender.account_display_name_needs_updating(row)
        assert result is None

    def test_account_display_name_needs_updating_true(self):
        row = ('357886268579', 'agseteam12')
        halo_csp_account_id = "920b3f30-9204-469a-967c-878aa4a77c06"
        halo_data = self.get_halo_account_data()
        csv_data = self.get_csv_update_data()
        blender = provisioner.Blender(halo_data, csv_data)
        result = blender.account_display_name_needs_updating(row)
        assert result == halo_csp_account_id

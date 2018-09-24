import cloudpassage
import provisioner
import pytest
import os

here_dir = os.path.abspath(os.path.dirname(__file__))
fixture_dir = os.path.join(here_dir, "../fixture")


class TestIntegrationHalo(object):
    def instantiate_halo_object(self, config):
        """Return an instance of the provisioner.Halo object."""
        return provisioner.Halo(config)

    def instantiate_config_object_nonworking(self):
        """Return a dummy, non-working config object."""
        conf_obj = provisioner.ConfigManager()
        conf_obj.halo_api_key = "ABC123"
        conf_obj.halo_api_secret_key = "DEF456"
        return conf_obj

    def test_instantiate_halo_object(self):
        """Instantiation will work, even with onoworking credentials."""
        config = self.instantiate_config_object_nonworking()
        assert self.instantiate_halo_object(config)

    def test_halo_object_sanity_fail(self):
        """Sanity check fails gracefully."""
        config = self.instantiate_config_object_nonworking()
        halo = self.instantiate_halo_object(config)
        with pytest.raises(SystemExit) as e:
            halo.sanity_check()
        assert e.type == SystemExit
        assert e.value.code == 1

    def test_halo_object_construct_arn(self):
        """Ensure role ARN is constructed correctly."""
        desired_result = "arn:aws:iam::065368812710:role/trusted-Newark"
        account_id = "065368812710"
        role_name = "trusted-Newark"
        actual_result = provisioner.Halo.construct_role_arn(account_id,
                                                            role_name)
        assert desired_result == actual_result

    def test_halo_validate_object_id_string_ok(self):
        """Well-formed ID passes."""
        testval = "92a11bcc905f11e896cb7f3cbd0e8cfd"
        retval = provisioner.Halo.validate_object_id(testval)
        assert retval is True

    def test_halo_validate_object_id_list_ok(self):
        """List of well-formed IDs pass."""
        testval = ["92a11bcc905f11e896cb7f3cbd0e8cfd",
                   "92a11bcc905f11e896cb7f3cbd0e8cfe"]
        retval = provisioner.Halo.validate_object_id(testval)
        assert retval is True

    def test_halo_validate_object_id_string_bad(self):
        """Badly-formed ID raises CloudPassageValidation."""
        testval = "92a11bcc905f11e896cb7f3cbd0../e8cfd"
        with pytest.raises(cloudpassage.CloudPassageValidation) as e:
            provisioner.Halo.validate_object_id(testval)
        assert e

    def test_halo_validate_object_id_list_bad(self):
        """Badly-formed ID raises CloudPassageValidation."""
        testval = ["92a11bcc905f11e896cb7f3cbd0e8cfd",
                   "92a11bcc905f11e896cb7f3cb../asde"]
        with pytest.raises(cloudpassage.CloudPassageValidation) as e:
            provisioner.Halo.validate_object_id(testval)
        assert e

    def test_halo_validate_object_id_type_bad(self):
        """Badly-formed ID raises CloudPassageValidation."""
        testval = {'onething': "92a11bcc905f11e896cb7f3cbd0e8cfd"}
        with pytest.raises(cloudpassage.CloudPassageValidation) as e:
            provisioner.Halo.validate_object_id(testval)
        assert e

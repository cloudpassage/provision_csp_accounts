#!/usr/bin/env python2.7
"""Bulk-provision AWS accounts."""
import provisioner


def main():
    # Instantiate config object and get settings from CLI args
    config = provisioner.ConfigManager()
    config.set_config_from_args()

    # Get a list of all CSP accounts managed by Halo
    halo = provisioner.Halo(config)
    halo.sanity_check()
    csp_accounts = halo.get_all_csp_accounts()

    # Get a list of account IDs and account display names from the CSV
    csv_consumer = provisioner.CsvConsumer(config)
    csv_tups = csv_consumer.get_account_metadata()

    # Get lists of accounts to be provisioned and updated
    blender = provisioner.Blender(csp_accounts, csv_tups)
    marching_orders = blender.create_change_set()

    # Perform provisioning in Halo
    print("Provisioning CSP accounts into Halo group %s with external ID %s." %
          (config.target_halo_group_id, config.external_id))
    for create_target in marching_orders["create"]:
        print("Provisioning account %s with display name %s" % create_target)
        if not config.dry_run:
            halo.provision_csp_account(create_target[0], create_target[1],
                                       config.role_name, config.external_id,
                                       config.target_halo_group_id)
    for update_target in marching_orders["update"]:
        print("Updating account %s with display name %s." % update_target)
        if not config.dry_run:
            halo.update_csp_display_name(update_target[0], update_target[1])
    return


if __name__ == "__main__":
    main()

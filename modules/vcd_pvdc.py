# Copyright © 2018 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

# !/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
client: pvdc

short_description: Provider VDC module for performing CRUD operation in vCloud Director

version_added: "2.4"

description:
    - This module is to create, read, update, delete PVDC in vCloud Director.
    - Task performed:
        - Create catalog
        - Read Catalog
        - Update name, description and shared state of catalog
        - Delete catalog

options:
    user:
        description:
            - vCloud Director user name
        required: false
    password:
        description:
            - vCloud Director user password
        required: false
    host:
        description:
            - vCloud Director host address
        required: false
    org:
        description:
            - Organization name on vCloud Director to access
        required: false
    api_version:
        description:
            - Pyvcloud API version
        required: false
    verify_ssl_certs:
        description:
            - whether to use secure connection to vCloud Director host
        required: false
    name:
        description:
            - catalog name
        required: true
    new_name:
        description:
            - new catalog name. Used while updating catalog name.
        required: false
    description:
        description:
            - description of the catalog
        required: false
    shared:
        description:
            - shared state of catalog(true/false)
        required: false
    state:
        description:
            - state of catalog ('present'/'absent').
            - One from state or operation has to be provided.
        required: false
    operation:
        description:
            - operation which should be performed over catalog.
            - various operations are:
                - updatenameanddescription : update catalog_name and catalog_description
                - sharecatalogstate : share or unshare catalog
                - readcatalog : read catalog metadata e.g catalog name, description, shared state of catalog
            - One from state or operation has to be provided.
        required: false

author:
    - pcpandey@mail.com
'''

EXAMPLES = '''
- name: create pvdc
  vcd_catalog:
    name: "name"
    description: "description"
    state: "present"
  register: output
'''

RETURN = '''
result: success/failure message relates to pvdc operation/operations
'''

from ansible.module_utils.vcd import VcdAnsibleModule
from pyvcloud.vcd.platform import Platform 


VCD_PVDC_STATES = ['present', 'absent']
VCD_PVDC_OPERATIONS = ['updatenameanddescription',
                          'sharecatalogstate', 'readcatalog']


def vcd_pvdc_argument_spec():
    return dict(
        name=dict(type='str', required=True),
        new_name=dict(type='str', required=False, default=''),
        description=dict(type='str', required=False, default=''),
        shared=dict(type='bool', required=False, default=False),
        state=dict(choices=VCD_PVDC_STATES, required=False),
        operation=dict(choices=VCD_PVDC_OPERATIONS, required=False)
    )

class PVDC(object):

    def __init__(self, module):
        self.module = module

    def get_vdc_object(self):
        pass

    def create(self):
        client = self.module.client
        params = self.module.params

        vim_server_name = params.get('vim_server_name')
        resource_pool_names = params.get('resource_pool_names')
        storage_profiles = params.get('storage_profiles')
        pvdc_name = params.get('pvdc_name')
        is_enabled = params.get('is_enabled')
        description = params.get('description')
        highest_hw_vers = params.get('highest_hw_vers')
        vxlan_network_pool = params.get('vxlan_network_pool')
        nsxt_manager_name = params.get('nsxt_manager_name')

        platform = Platform(client)
        platform.create_provider_vdc(self,
                            vim_server_name,
                            resource_pool_names,
                            storage_profiles,
                            pvdc_name,
                            is_enabled,
                            description,
                            highest_hw_vers,
                            vxlan_network_pool,
                            nsxt_manager_name)

    def read(self):
        pass
    
    def update(self):
        pass
    
    def delete(self):
        pass
    

def manage_states(pvdc):
    state = pvdc.module.params.get('state')

    if state == "present":
        return pvdc.create()
    elif state == "absent":
        return pvdc.delete()


def manage_operations(pvdc):
    operation = pvdc.module.params.get('operation')

    if (operation == "updatenameanddescription"):
        return pvdc.update_name_and_description()

    if operation == "sharecatalogstate":
        return pvdc.share()

    if operation == "readcatalog":
        return pvdc.read()


def main():
    argument_spec = vcd_pvdc_argument_spec()

    response = dict(
        msg=dict(type='str'),
        changed=False,
    )

    module = VcdAnsibleModule(argument_spec=argument_spec,
                              supports_check_mode=True)
    try:
        pvdc = PVDC(module)
        if module.params.get('state'):
            response = manage_states(pvdc)
        elif module.params.get('operation'):
            response = manage_operations(pvdc)
        else:
            raise Exception('One of from state/operation should be provided.')
    except Exception as error:
        response['msg'] = error.__str__()
        module.fail_json(**response)

    module.exit_json(**response)


if __name__ == '__main__':
    main()


#Platform
#VDC of pyvcloud

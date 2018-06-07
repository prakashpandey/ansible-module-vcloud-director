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
        - Create provider vdc
        - Reload provider vdc
        - Set provider vdc metadata

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
    pvdc_name:
        description:
            - catalog name
        required: true
    state:
        description:
            - state of pvdc ('present'/'absent').
            - One from state or operation has to be provided.
        required: false
    operation:
        description:
            - operation which should be performed over pvdc.
            - various operations are:
                - setmetadata : set provider vdc metadata
                - reload : reload provider vdc
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
from pyvcloud.vcd.pvdc import PVDC 


VCD_PVDC_STATES = ['present', 'absent']
VCD_PVDC_OPERATIONS = ['setmetadata', 'reload']


def vcd_pvdc_argument_spec():
    return dict(
        pvdc_name=dict(type='str', required=True),
        shared=dict(type='bool', required=False, default=False),
        state=dict(choices=VCD_PVDC_STATES, required=False),
        operation=dict(choices=VCD_PVDC_OPERATIONS, required=False)
    )

class VcdPVDC(object):

    def __init__(self, module):
        self.module = module

    def get_vdc_object(self):
        pvdc = PVDC()
        return pvdc

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
        response = dict()

        platform = Platform(client)
        platform.create_provider_vdc(vim_server_name = vim_server_name,
                            resource_pool_names = resource_pool_names,
                            storage_profiles = storage_profiles,
                            pvdc_name = pvdc_name,
                            is_enabled = is_enabled,
                            description = description,
                            highest_hw_vers = highest_hw_vers,
                            vxlan_network_pool = vxlan_network_pool,
                            nsxt_manager_name = nsxt_manager_name
                            )
        response['msg'] = 'Pvdc {} has been created.'.format(pvdc_name)
        response['changed'] = True

        return response
        
    
    def reload(self):
        pvdc_name = self.params.get('pvdc_name')
        response = dict()

        pvdc = self.get_vdc_object()
        pvdc.reload()
        response['msg'] = 'Pvdc {} has been reloaded.'.format(pvdc_name)
        response['changed'] = True

        return response

    def get_metadata(self):
        pvdc = self.get_vdc_object()
        metadata = pvdc.get_metadata()
        return metadata

    def set_metadata(self):
        params = self.params
        pvdc_name = params.get('pvdc_name')
        domain = params.get('domain')
        visibility = params.get('visibility')
        key = params.get('key')
        value = params.get('value')
        metadata_type = params.get('metadata_type')
        response = dict()

        pvdc = self.get_vdc_object()
        pvdc.set_metadata(
            domain = domain,
            visibility = visibility,
            key = key,
            value = value,
            metadata_type = metadata_type
        )
        response['msg'] = 'Pvdc {} metadata has been set.'.format(pvdc_name)
        response['changed'] = True

        return response
    
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

    if (operation == "setmetadata"):
        return pvdc.set_metadata()

    if operation == "reload":
        return pvdc.reload()



def main():
    argument_spec = vcd_pvdc_argument_spec()

    response = dict(
        msg=dict(type='str'),
        changed=False,
    )

    module = VcdAnsibleModule(argument_spec=argument_spec,
                              supports_check_mode=True)
    try:
        pvdc = VcdPVDC(module)
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

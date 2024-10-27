#!/home/ubuntu/ansible-config-mgt/ansible_env/bin/python3

import boto3
import json

def get_ec2_instances():
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.all()
    
    inventory = {
        '_meta': {
            'hostvars': {}
        }
    }

    for instance in instances:
        if instance.state['Name'] == 'running':
            group = instance.tags[0]['Value'] if instance.tags else 'ungrouped'
            if group not in inventory:
                inventory[group] = {
                    'hosts': [],
                    'vars': {}
                }
            inventory[group]['hosts'].append(instance.private_ip_address)
            inventory['_meta']['hostvars'][instance.private_ip_address] = {
                'ansible_host': instance.private_ip_address,
                'ansible_user': 'ec2-user',
                'ansible_ssh_private_key_file': "/home/ubuntu/.ssh/Bukasiation's-SSH-Key.pem"
            }

    return inventory

if __name__ == '__main__':
    print(json.dumps(get_ec2_instances(), indent=2))
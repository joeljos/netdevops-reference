#!/usr/bin/env bash

ansible-playbook Ansible/ospfv2/rollback_router1_ospfv2.yaml
ansible-playbook Ansible/ospfv2/rollback_router2_ospfv2.yaml
ansible-playbook Ansible/ospfv2/rollback_switch1_ospfv2.yaml
ansible-playbook Ansible/ospfv2/rollback_asa_ospfv2.yaml
ansible-playbook Ansible/ospfv2/rollback_switch2_ospfv2.yaml
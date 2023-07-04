#!/usr/bin/env bash

ansible-playbook Ansible/ospfv2/router1_ospfv2.yaml
ansible-playbook Ansible/ospfv2/router2_ospfv2.yaml
ansible-playbook Ansible/ospfv2/switch1_ospfv2.yaml
ansible-playbook Ansible/ospfv2/asa_ospfv2.yaml
ansible-playbook Ansible/ospfv2/switch2_ospfv2.yaml
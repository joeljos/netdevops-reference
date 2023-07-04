#!/usr/bin/env bash

ansible-playbook Ansible/directInterface/router1_directInterface.yaml
ansible-playbook Ansible/directInterface/router2_directInterface.yaml
ansible-playbook Ansible/directInterface/switch1_directInterface.yaml
ansible-playbook Ansible/directInterface/asa_directInterface.yaml
ansible-playbook Ansible/directInterface/switch2_directInterface.yaml
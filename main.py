import sys
import django
import boto3
import re
import time
import os

sys.dont_write_bytecode = True
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
initialized = False
django.setup()

from db.models import *

from python_terraform import *

def create_nmap_instance(region='us-east-2', sg=['sg-000'], subnet='subnet-000', hosts=['1.1.1.1']):
    i = EC2Instance.objects.filter(secgroups=sg[0])
    for scount in range(0, len(sg)):
        i = i.filter(secgroups=sg[scount])
    print('[i] Mimcking instance %s (%s)' % (i[0], i[0].private))
    print('[i] Staging scan environment for %s/%s/%s' % (region, subnet, ','.join(sg)))
    global initialized
    t = Terraform(working_dir='.')
    if not initialized:
        t.init()
        initialized = True
    code, result, err = t.apply(
        var={'region': region, 'sg': sg, 'subnet': subnet, 'hosts':hosts},
        skip_plan=True,
        no_color=IsFlagged
        )
    try:
        instance = re.search('complete after.+\[id=([a-z\-0-9]+)\]', result).group(1) 
        print('[+] Terraform apply was successful: %s ' % instance)
        return instance
    except AttributeError:
        print("[!] No changes applied.")
        print(code, result, err)
        pass
    t.destroy(input=False, no_color=IsFlagged)
    return None

def get_output(id):
    ec2_client = boto3.client('ec2')
    out = ''
    print('[i] Waiting for scan results...')
    while re.search(".*--- SCAN END ---.*", out) is None:
        try:
            out = ec2_client.get_console_output(InstanceId=id, Latest=True)['Output']
        except KeyError:
            out = ''
        time.sleep(1)
    try:
        scan = re.search('(?<=--- SCAN START ---\n)(.*\n)+(?=.*--- SCAN END ---)', out).group(0)
        scan = re.sub(r'^.*cloud-init\[[0-9]+\]:\s', '', scan)
    except AttributeError:
        print("[!] Error getting scan output.")
        raise
    return scan

def get_vpc_data(id):
    ec2_resource = boto3.resource('ec2')
    vpc = ec2_resource.Vpc(id)
    return vpc

def get_subnet_data(id):
    ec2_resource = boto3.resource('ec2')
    vpc = ec2_resource.Subnet(id)
    return vpc

def get_public_ip(interfaces):
    public = ''
    for intf in interfaces:
        if 'Association' in intf:
            public = intf['Association']['PublicIp']
    return public

def list_resources():
    for v in VPCInstance.objects.all():
            print('\n[+] Found VPC: %s (%s)' % (v, v.cidr))
            print('Subnets:')
            for s in v.subnets.all():
                print('(S) %s (%s)' % (s,s.cidr))
                print('\tEC2 Instances:')
                for i in s.instances.all():
                    print('\t(I) %s (%s)' % (i, i.private))
                    print('\t\tSecurity Groups:')
                    for sg in i.secgroups.all():
                        print('\t\t(G) %s (%s)' % (sg.name, sg))
            print('\n')

def get_options():
    options = list()
    for v in VPCInstance.objects.all():
        for s in v.subnets.all():
            for i in s.instances.all():
                options.append('%s/%s/%s' % (v.region, s, ','.join(list(i.secgroups.values_list('id', flat=True)))))
    poss = list(set(options))
    print('[i] Initiating scans for following combinations:\n%s\n' % '\n'.join(poss))
    return [p.split('/') for p in poss]

def get_targets():
    return list(EC2Instance.objects.values_list('private', flat=True))

def get_instance_data():

    print('[i] Scanning for resources...')

    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_instances()

    for reserv in response['Reservations']:
        for instance in reserv['Instances']:
            try:
                public = ''
                vpc_data = get_vpc_data(instance['VpcId'])
                vpc, created = VPCInstance.objects.get_or_create(
                    id=instance['VpcId'],
                    cidr=vpc_data.cidr_block,
                    region=ec2_client.meta.region_name
                    )
                subnet_data = get_subnet_data(instance['SubnetId'])
                subnet, created = SubnetInstance.objects.get_or_create(
                    id=instance['SubnetId'],
                    vpc=vpc,
                    cidr=subnet_data.cidr_block
                    )
                
                ec2, created = EC2Instance.objects.get_or_create(
                    id=instance['InstanceId'],
                    private=instance['PrivateIpAddress'],
                    public=get_public_ip(instance['NetworkInterfaces']),
                    subnet=subnet
                    )

                for secgroup in instance['SecurityGroups']:
                    sg, created = SecGroupInstance.objects.get_or_create(id=secgroup['GroupId'], name=secgroup['GroupName'])
                    ec2.secgroups.add(sg)
            except KeyError as e:
                pass

try:
    get_instance_data()
    list_resources() 
    targets = get_targets()
    options = get_options()
    for o in options:
        ec2 = create_nmap_instance(region=o[0], subnet=o[1], sg=o[2].split(','), hosts=targets)
        if not ec2:
            print("[!] Terraform failed to apply changes")
            exit(1)
        scan = get_output(ec2)
        print("[+] Completed scan for %s (%s/%s/%s)\n" % (ec2, o[0], o[1], o[2]))
        print(scan)
        print('Cleaning up...')
        t = Terraform(working_dir='.')
        t.destroy(input=False, no_color=IsFlagged)
except KeyboardInterrupt:
    print('Cleaning up...')
    t = Terraform(working_dir='.')
    t.destroy(input=False, no_color=IsFlagged)

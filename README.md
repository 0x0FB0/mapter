# mapter
AWS subnet scanner automated with terraform

----
This tool tries to solve the challenge of network access control validation throughout the security group and subnet matrix.
It tries to mimic existing EC2 instances and launch network scans from various points of cloud infrastructure.

This is merely a result of learning Terraform and AWS cloud API. Many functionalities have been limited (i.e. netcat used instead of nmap due to lack of built-in package in AMI)

### Dependencies
- AWS CLI
- Terraform
- Python 3
- boto3
- Django Framework

### Example output
```
[i] Scanning for resources...

[+] Found VPC: vpc-0318ff1396617c8e9 (10.1.1.0/24)
Subnets:
(S) subnet-09d7b5791c5424b87 (10.1.1.192/28)
        EC2 Instances:
        (I) i-025cab45f607469b3 (10.1.1.198)
                Security Groups:
                (G) launch-wizard-4 (sg-099cdc581de3c2808)

[+] Found VPC: vpc-09159a62 (172.31.0.0/16)
Subnets:
(S) subnet-57b7e31b (172.31.32.0/20)
        EC2 Instances:
        (I) i-08503dc1ac5431965 (172.31.34.206)
                Security Groups:
                (G) launch-wizard-1 (sg-02beb09f2953b3c2c)
        (I) i-04a38c6f678c7f8ca (172.31.38.64)
                Security Groups:
                (G) launch-wizard-3 (sg-00ffe84e40ca7f7f0)
                (G) launch-wizard-2 (sg-017de5d715c72ef74)
        (I) i-09ffff02fcdd9c08f (172.31.41.56)
                Security Groups:
                (G) launch-wizard-2 (sg-017de5d715c72ef74)
        (I) i-029724174f6b00032 (172.31.43.189)
                Security Groups:
                (G) launch-wizard-1 (sg-02beb09f2953b3c2c)
        (I) i-01f67e1f945e5237f (172.31.42.12)
                Security Groups:
                (G) launch-wizard-3 (sg-00ffe84e40ca7f7f0)
        (I) i-0b105d106f783b0ff (172.31.37.238)
                Security Groups:
                (G) launch-wizard-3 (sg-00ffe84e40ca7f7f0)
(S) subnet-05390621bf23b43f3 (172.31.1.0/24)
        EC2 Instances:
        (I) i-0700d1709c8e72cb7 (172.31.1.103)
                Security Groups:
                (G) newone (sg-00bdd6211ce8201d3)
                (G) launch-wizard-3 (sg-00ffe84e40ca7f7f0)
        (I) i-0c88240fdb5329fcf (172.31.1.139)
                Security Groups:
                (G) newone (sg-00bdd6211ce8201d3)
        (I) i-024862f619dee0d7d (172.31.1.143)
                Security Groups:
                (G) newone (sg-00bdd6211ce8201d3)
        (I) i-078b1f6176477d334 (172.31.1.195)
                Security Groups:
                (G) newone (sg-00bdd6211ce8201d3)


[i] Initiating scans for following combinations:
us-east-2/subnet-05390621bf23b43f3/sg-00bdd6211ce8201d3
us-east-2/subnet-57b7e31b/sg-02beb09f2953b3c2c
us-east-2/subnet-57b7e31b/sg-017de5d715c72ef74
us-east-2/subnet-09d7b5791c5424b87/sg-099cdc581de3c2808
us-east-2/subnet-05390621bf23b43f3/sg-00bdd6211ce8201d3,sg-00ffe84e40ca7f7f0
us-east-2/subnet-57b7e31b/sg-00ffe84e40ca7f7f0,sg-017de5d715c72ef74
us-east-2/subnet-57b7e31b/sg-00ffe84e40ca7f7f0

<snip>

[i] Mimcking instance i-0700d1709c8e72cb7 (172.31.1.103)
[i] Staging scan environment for us-east-2/subnet-05390621bf23b43f3/sg-00bdd6211ce8201d3,sg-00ffe84e40ca7f7f0
[+] Terraform apply was successful: i-055211e8bac1089e4 
[i] Waiting for scan results...
[+] Got results (len: 3658)
[+] Completed scan for i-055211e8bac1089e4 (us-east-2/subnet-05390621bf23b43f3/sg-00bdd6211ce8201d3,sg-00ffe84e40ca7f7f0)

Simple netcat port scan for hosts 10.1.1.198,172.31.34.206,172.31.38.64,172.31.1.103,172.31.41.56,172.31.1.139,172.31.43.189,172.31.1.143,172.31.42.12,172.31.1.195,172.31.37.238
nc: connect to 10.1.1.198 port 22 (tcp) timed out: Operation now in progress
nc: connect to 172.31.34.206 port 22 (tcp) timed out: Operation now in progress
Connection to 172.31.38.64 22 port [tcp/ssh] succeeded!
nc: connect to 172.31.1.103 port 22 (tcp) timed out: Operation now in progress
<snip>

[i] Mimcking instance i-04a38c6f678c7f8ca (172.31.38.64)
[i] Staging scan environment for us-east-2/subnet-57b7e31b/sg-00ffe84e40ca7f7f0,sg-017de5d715c72ef74
[+] Terraform apply was successful: i-0e9d6609573541a7b 
[i] Waiting for scan results...
[+] Got results (len: 3658)
[+] Completed scan for i-0e9d6609573541a7b (us-east-2/subnet-57b7e31b/sg-00ffe84e40ca7f7f0,sg-017de5d715c72ef74)

Simple netcat port scan for hosts 10.1.1.198,172.31.34.206,172.31.38.64,172.31.1.103,172.31.41.56,172.31.1.139,172.31.43.189,172.31.1.143,172.31.42.12,172.31.1.195,172.31.37.238
nc: connect to 10.1.1.198 port 22 (tcp) timed out: Operation now in progress
nc: connect to 172.31.34.206 port 22 (tcp) timed out: Operation now in progress
Connection to 172.31.38.64 22 port [tcp/ssh] succeeded!
nc: connect to 172.31.1.103 port 22 (tcp) timed out: Operation now in progress
nc: connect to 172.31.41.56 port 22 (tcp) timed out: Operation now in progress
nc: connect to 172.31.1.139 port 22 (tcp) timed out: Operation now in progress
nc: connect to 172.31.43.189 port 22 (tcp) timed out: Operation now in progress
nc: connect to 172.31.1.143 port 22 (tcp) timed out: Operation now in progress
nc: connect to 172.31.42.12 port 22 (tcp) timed out: Operation now in progress
nc: connect to 172.31.1.195 port 22 (tcp) timed out: Operation now in progress
nc: connect to 172.31.37.238 port 22 (tcp) timed out: Operation now in progress
nc: connect to 10.1.1.198 port 80 (tcp) timed out: Operation now in progress
nc: connect to 172.31.34.206 port 80 (tcp) failed: Connection refused
nc: connect to 172.31.38.64 port 80 (tcp) timed out: Operation now in progress
nc: connect to 172.31.1.103 port 80 (tcp) timed out: Operation now in progress
<snip>

Cleaning up...
```
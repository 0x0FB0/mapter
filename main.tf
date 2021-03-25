variable "region" {
    default = "us-east-2"
}
variable "sg" {
    default = ["sg-000", "sg-001"]
}
variable "subnet" {
    default = "subnet-000"
}
variable "hosts" {
    default = ["1.1.1.1", "2.2.2.2"]
}

// nmap is not preinstalled by default
// as ec2 might not have the internet access this might not work
// workaround would be to subscribe to kali-linux in AWS marketplace
variable "nmap_template" {
    default = <<EOF
        #!/bin/bash -v
        yum install nmap
        echo "--- SCAN START ---"
        echo "Simple nmap port scan for hosts %s"
        nmap -Pn -n -F -sS -sV -sC %s
        echo "--- SCAN END ---"
    EOF
}

variable "netcat_template" {
    default = <<EOF
        #!/bin/bash -v
        ports="22,80,443,8080"
        echo "--- SCAN START ---"
        echo "Simple netcat port scan for hosts %s"
        echo "$ports" | tr "," "\n" | while read pp
        do echo "%s" | tr "," "\n" | while read hh
            do nc  -w 1 -vz $hh $pp
            done
        done
        echo "--- SCAN END ---"
    EOF
}

data "aws_ami" "amazon-linux" {
  most_recent = true

    filter {
        name   = "owner-alias"
        values = ["amazon"]
    }


    filter {
        name   = "name"
        values = ["*2018.03*"]
    }

    owners = ["amazon"]
}

provider "aws" {
    profile = "default"
    region = var.region
}

// the only way to run scan without public IP on EC2
// will cause terraform to rebuild the whole instance (takes looong time)
data "cloudinit_config" "config" {
  gzip          = false
  base64_encode = true

  part {
    content_type = "text/x-shellscript"
    filename = "scan.sh"
    content = format(var.netcat_template, join(",", var.hosts), join(",", var.hosts))
  }
}

resource "aws_instance" "nmap_box" {
    ami = data.aws_ami.amazon-linux.id
    instance_type = "t3.micro"
    vpc_security_group_ids = var.sg
    associate_public_ip_address = false
    tags = { name = "pentest"}
    subnet_id = var.subnet
    user_data_base64  = data.cloudinit_config.config.rendered
}
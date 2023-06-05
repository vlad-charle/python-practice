provider "aws" {}

# IP var should be provided via tf CLI command execution, i.e. terraform plan -var 'my_ip=192.158.1.38/32'
variable "my_ip" {}

data "aws_vpc" "get_vpc" {
  default = true
}

data "aws_subnets" "get_subnets" {
  filter {
    name   = "default-for-az"
    values = [true]
  }
}

data "aws_subnet" "subnet_ids" {
  for_each = toset(data.aws_subnets.get_subnets.ids)
  id       = each.value
}

locals {
  subnets_ids = [for subnet in data.aws_subnet.subnet_ids : subnet.id]
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_key_pair" "ec2_ssh_key" {
  key_name   = "ec2-key"
  public_key = file("~/.ssh/id_rsa.pub")
}

resource "aws_security_group" "ssh_80" {
  name        = "ssh-8080"
  description = "Allow SSH and port 8080"
  vpc_id      = data.aws_vpc.get_vpc.id

  ingress {
    description = "Nginx port 80"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  lifecycle {
    create_before_destroy = true
  }
}


resource "aws_instance" "server" {
  count                       = 3
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.micro"
  associate_public_ip_address = true
  key_name                    = aws_key_pair.ec2_ssh_key.key_name
  subnet_id                   = local.subnets_ids[0]
  user_data                   = <<EOF
#!/bin/bash

# install Docker Engine
apt-get update && apt-get install -y ca-certificates curl gnupg
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo \
"deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
"$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update && apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
docker -v
EOF
  vpc_security_group_ids      = [aws_security_group.ssh_80.id]
  tags = {
    Name = "my-custom-nginx"
  }
}

output "ec2_ips" {
  value = aws_instance.server[*].public_ip
}
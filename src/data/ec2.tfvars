configuration = [
  {
    "id" : "web1",
    "name" : "web1",
    "type" : "t2.micro",
    "region" : "us-east-2",
    "subnet_id" : "subnet-0d7282b757dddab53",
    "ami_id" : "ami-00a9282ce3b5ddfb1",
    "ami_filter" : "N/A",
    "root_block_device" : {
      "device_name" : "/dev/xvda",
      "volume_size" : "8",
      "volume_type" : "gp3"
    },
    "ebs_block_devices" : [
      {
        "device_name" : "/dev/sdb",
        "volume_size" : "1",
        "volume_type" : "gp3"
      }
    ]
  }
]

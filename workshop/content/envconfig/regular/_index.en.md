+++
title = "Regular AWS Account"
date = 2020-05-28T19:03:45-07:00
weight = 10
chapter= true
+++

If you're using your own AWS account, or you are advised by AWS staff to configure the workshop environment, you need to setup some resources on AWS that we will use to perfrom the migration. This section describes the steps to provision the AWS resources that are required for this database migration walkthrough. 

We use [AWS CloudFormation](https://aws.amazon.com/cloudformation/) to simplify the provisioning of the infrastructure, so we can concentrate on tasks related to data migration. 


{{% notice warning  %}}
The resources provisined as part of this workshop will incur charges. Remember to use the [Environment Cleanup](../../en/envclean.html) guide **after** you have completed the workshop to stop incurring additional costs. 
{{% /notice %}}

---
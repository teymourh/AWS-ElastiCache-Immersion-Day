+++
title = "Configure the Environment"
date = 2019-12-20T13:13:22-08:00
weight = 23
+++
___

In this step, you will use a CloudFormation (CFN) template to deploy the infrastructure for this database migration. [AWS CloudFormation](https://aws.amazon.com/cloudformation/) simplifies provisioning the infrastructure, so we can concentrate on tasks related to data migration. 

5. Open the AWS CloudFormation [console](https://console.aws.amazon.com/cloudformation/), and click on **Create Stack** in the left-hand corner.

	![\[create-stack\]](/images/screenshots/EnvConfig04.png)

6. Select Template is ready, and choose Upload a template file as the source template. Then, click on **Choose file** and upload the [ee-elc-lab-v4.yaml ](/code/ee-elc-lab-v4.yaml ). Click **Next**.

	![\[add-template\]](/images/screenshots/EnvConfig05.png)

7. Populate the form as with the values specified below, and then click **Next**.

	| **Input Parameter** | **Values** |
	| ------ | ------ |
	| **EEKeyPair** | The EC2 keypair you created in the previous section. |
	| **DatabaseUser** | Database user name for MySQL database. |
	| **DatabasePassword** | Database password for MySQL database. Note: password complexity requires at least 6 characters!|

{{% notice warning %}}
The resources that are created here will be prefixed with whatever value you specify in the Stack Name.  Please specify a value that is **unique** to your account.
{{% /notice %}} 

{{% notice info %}}
Depending on the type of  workshop that you are completing, you may get a different set of parameters that can vary from the above screenshot.
{{% /notice %}}

![\[input-parameters\]](/images/screenshots/EnvConfig06.png)

8. On the **Stack Options** page, accept all of the defaults and click **Next**.

9. On the **Review** page, click **Create stack**.

	![\[review-stack\]](/images/screenshots/EnvConfig07.png)

10.	At this point, you will be directed back to the CloudFormation console and will see a status of **CREATE_IN_PROGRESS**.  Please wait here until the status changes to **COMPLETE**.

	![\[stack-progress\]](/images/screenshots/EnvConfig08.png)

11.	Once CloudFormation status changes to **CREATE_COMPLETE**, go to the **Outputs** section.

12.	Make a note of the **Output** values from the CloudFormation environment that you launched as you will need them for the remainder of the tutorial
___

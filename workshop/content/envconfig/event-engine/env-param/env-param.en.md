+++
title = "Get the Environment Parameters"
date = 2020-05-28T18:47:43-07:00
weight = 15
+++

---

6. Once you have opened the AWS Management Console for the first time, Make sure you are remaining in the designated AWS Region. If you're in a different region, please change the region from the top right conrner of the screen to the designated region. 

7. Navigate to [AWS CloudFormation](https://console.aws.amazon.com/cloudformation/) and click on the `mod-XXXXXXXXXXXXXXXX` stack. 

	![CloudFormation Stack List](/images/screenshots/cfn-stack-list.png)

8. If the status of the stack is `CREATE_COMPLETE`, click on the **Outputs** tab. Take a note of these values in a notepad that you have easy access to, as they will be critical to the completion of the remainder of the lab. 

	![CloudFormation Output](/images/screenshots/EnvConfig10.png)

{{% notice info %}}
Depending on the type of migration workshop that you are completing, you may get a different set of Output variables that can vary from the above screenshot.
{{% /notice %}}


---
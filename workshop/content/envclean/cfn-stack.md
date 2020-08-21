+++
title = "Delete the CloudFormation Stack"
date = 2019-12-20T18:16:08-08:00
weight = 54
+++

---

If you are using an EventEngine or JAMS account provided by AWS you can skip this section. Otherwise, if you configured the resources using the AWS CloudFormation template listed in the Getting Started section you can clean up resources by deleting the CloudFormation stack:

13.	Go to the CloudFormation [console](https://console.aws.amazon.com/cloudformation/), and click select the **CloudFormation Stack** that you created during the workshop. 

14.	Click on the **Delete** button from the top right corner. CloudFormation will automatically remove all resources that it launched earlier. This process can take up to 15 minutes. 

	![\[cfn-stack1\]](/images/screenshots/EnvCleanup10.png)
  
15.	Confirm that you want to delete the stack.

	![\[cfn-stack2\]](/images/screenshots/EnvCleanup11.png)

16.	Check the CloudFormation console to ensure the stack that you selected is removed.  

You have completed removing the AWS resources that you created earlier in your account.

---
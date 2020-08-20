+++
title = "Download the EC2 Key Pair"
date = 2020-05-28T18:32:44-07:00
weight = 10
+++

---

4. On your browser, return to [Event Engine Dashboard](https://dashboard.eventengine.run/), you should be back on the **Team Dashboard**, click on **SSH Key**.

	![Event Engine SSH Key](/images/screenshots/ee-ssh1.png?height=30pc)

5. Click on the **Download Key** button. This will download the .pem file.

	![Event Engine SSH Key](/images/screenshots/ee-ssh2.png?height=35pc)

Remember the location that you saved the pem keypair file on your computer. You will use this file later to decrypt the Windows login password in order to log on to the remote desktop.

{{% notice info %}}
We use Remote Desktop Protocol (RDP) to connect to the Amazon EC2 Instance. Please ensure you have a RDP client such as [Microsoft Remote Desktop](https://docs.microsoft.com/en-us/windows-server/remote/remote-desktop-services/clients/remote-desktop-clients) installed on your workstation. 
{{% /notice %}}


---
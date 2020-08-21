+++
title = "Download the EC2 Key Pair"
date = 2020-05-28T18:32:44-07:00
weight = 3
+++

---

On the challenge dashboard click the "SSH Key Pair" button to download the key pair. 

{{% img "JamsKeyPair.png" "Download SSH keypair" %}}

Remember the location that you saved the pem keypair file on your computer. You will use this file later to access virtual machines via SSH or to decrypt the Windows login password in order to log on to the remote desktop.

{{% notice info %}}
We use Remote Desktop Protocol (RDP) to connect to the Amazon EC2 Instance. Please ensure you have a RDP client such as [Microsoft Remote Desktop](https://docs.microsoft.com/en-us/windows-server/remote/remote-desktop-services/clients/remote-desktop-clients) installed on your workstation. 
{{% /notice %}}

{{% notice warning %}}
The default name of the key pair for JAMS challenges is `lab-key-pair`. If you perform multiple challenges that require key pairs, these may be named the same but be different key pairs. We recommend that you verify that you are using the key pair for the current challenge.
{{% /notice %}}

---
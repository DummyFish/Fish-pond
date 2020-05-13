# Fish-pond

In the security field, it is always harder to defend than attack, especially for those who don’t have enough knowledge to protect their network. Thus, we proposed a honeypot as a countermeasure that could be deployed in the local network and stop attackers from compromising it.
We believe that such a specialized honeypot could protect privacy as well as tools to analyze attackers’ attacks. People could benefit from hiding their real data behind a decoy and isolating potential damage.
Our project can help detect malicious traffic into our devices. It can help any person to defend their devices from malicious users, protect their personal data.

We plan to build a honeypot with the following features:
Main Features:
  - Check local network devices' vulnerabilities.
  - Notify users if any attackers try to compromise the network.
  - Logging any malicious activities on the honey pot.

Details:
  - The honey pot would scan the local network and detect vulnerabilities in the local network.

  - The services covered by the honey pot could be either fake services or actual modified services.
    - e.g., MySQL, ssh, FTP, telnet

  - Faking some famous services and websites.
    - e.g., Wordpress

  - Logs would be presented in both text format or through visualization.
    - Logging username and password tried on the honey pot.
    - Logging command used by attackers.
    - Logging attackers' IP.
    - Logging category of attacks.
    - An administration interface would be provided.
        - The administration interface offers detailed statistics information about logs through visualization. 
        - Geo visualize attackers’ IP
        - Sub panels for different services

  - Notification
    - Local network vulnerabilities.
    - Any malicious activities.
    - send emails to the user   

We expect to build an identical administrative website so that we can attract more malicious users. We expect thousands of connection attempts from multiple services such as ssh, FTP, and etc across the globe. We will visualize the result from our logging data.

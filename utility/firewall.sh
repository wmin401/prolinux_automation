firewall-cmd --add-port=111/tcp
firewall-cmd --add-port=892/tcp
firewall-cmd --add-port=2049/tcp
firewall-cmd --add-port=32803/tcp
firewall-cmd --add-port=111/udp
firewall-cmd --add-port=892/udp
firewall-cmd --add-port=2049/udp
firewall-cmd --add-port=32803/udp
firewall-cmd --reload
firewall-cmd --list-all
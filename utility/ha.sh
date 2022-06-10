firewall-cmd --permanent --add-service=high-availability
firewall-cmd --zone=public --permanent --add-port=2224/tcp
firewall-cmd --zone=public --permanent --add-port=3121/tcp
firewall-cmd --zone=public --permanent --add-port=5403/tcp
firewall-cmd --zone=public --permanent --add-port=21064/tcp
firewall-cmd --zone=public --permanent --add-port=9929/tcp
firewall-cmd --zone=public --permanent --add-port=5504/udp
firewall-cmd --zone=public --permanent --add-port=5505/udp
firewall-cmd --zone=public --permanent --add-port=9929/udp
firewall-cmd --reload
firewall-cmd --list-all

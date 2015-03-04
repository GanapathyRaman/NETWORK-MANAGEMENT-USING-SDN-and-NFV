#Confguration Specific to CompanyA

#@author: Sikandar Khan

echo "Openrc CompanyA"
. ./openrc CompanyA CompanyA

echo "Creating networks in CompanyA" 
echo "Launching 10.0.0.0/24 network in companyA"
neutron net-create CompanyAwebserverNetwork --tenant_id $(keystone tenant-list | grep '\sCompanyA' | awk '{print $2}')
neutron subnet-create CompanyAwebserverNetwork 10.0.0.0/24 --name CompanyAwebserverNetwork

echo "Launching 20.0.0.0/24 network in CompanyA" 
neutron net-create CompanyAproxyserverNetwork --tenant_id $(keystone tenant-list | grep '\sCompanyA' | awk '{print $2}')
neutron subnet-create CompanyAproxyserverNetwork 30.0.0.0/24 --name CompanyAproxyserverNetwork

echo "Creating routers on CompanyA"
neutron router-create R-CompAwebServer
neutron router-create R-CompAproxy

echo "Adding Pubic Gateway for R-CompAwebServer public"
neutron router-gateway-set R-CompAwebServer public

echo "Attaching interface of R-CompAwebServer to network CompanyAwebserverNetwork"
neutron router-interface-add R-CompAwebServer $(neutron subnet-list | grep  CompanyAwebserverNetwork | awk '{print $2}')

echo "Adding Pubic Gateway for R-CompAwebServer public"
neutron router-gateway-set R-CompAproxy public

echo "Attaching interface of R-CompAproxy to network CompanyAproxyserverNetwork"
neutron router-interface-add R-CompAproxy $(neutron subnet-list | grep CompanyAproxyserverNetwork | awk '{print $2}')

echo "Exporting image" 
export IMAGE=TinyCore

echo "Launching Instances"
nova boot --flavor m1.tiny --image $(nova image-list | grep $IMAGE'\s' | awk '{print $2}') --nic net-id=$(neutron net-list | grep CompanyAwebserverNetwork | awk '{print $2}') CA-Webserver1 --availability_zone=sak:sak
nova boot --flavor m1.tiny --image $(nova image-list | grep $IMAGE'\s' | awk '{print $2}') --nic net-id=$(neutron net-list | grep CompanyAwebserverNetwork | awk '{print $2}') CA-Webserver2 --availability_zone=sak:sak
nova boot --flavor m1.tiny --image $(nova image-list | grep $IMAGE'\s' | awk '{print $2}') --nic net-id=$(neutron net-list | grep CompanyAproxyserverNetwork | awk '{print $2}') CA-ProxyServer --availability_zone=sak:sak

#Adding Security Rules
echo "Adding Security Rules for CompanyA"

echo "Adding ICMP Rule for CompanyA"
nova secgroup-add-rule default icmp -1 -1 0.0.0.0/0

echo "Adding TCP Rule for CompanyA"
nova secgroup-add-rule default tcp 1 65535 0.0.0.0/0

#Load Balancer for CompanyA
echo "Creating Load Balancing Pool for CompanyA"
neutron lb-pool-create --lb-method ROUND_ROBIN --name companyApool --protocol HTTP --subnet-id $(neutron subnet-list | grep CompanyAwebserverNetwork | awk '{print $2}')

echo "Creating WebServer's to the pool"
neutron lb-member-create --address  $(nova list | grep CA-Webserver1 | awk '{print $12}' | cut -d "=" -f 2) --protocol-port 80 companyApool
neutron lb-member-create --address  $(nova list | grep CA-Webserver2 | awk '{print $12}' | cut -d "=" -f 2) --protocol-port 80 companyApool

echo "Assigning VIP to the Load Balancer of the CompanyA"
neutron lb-vip-create --name companyAvip --protocol-port 80 --protocol HTTP --subnet-id $(neutron subnet-list | grep CompanyAwebserverNetwork | awk '{print $2}') companyApool

#CompanyA VPN Configurations

echo "Adding IKE Policy to CompanyA"
neutron vpn-ikepolicy-create companyAikepolicy

echo "Adding IPSec Policy to CompanyA"
neutron vpn-ipsecpolicy-create companyAipsecpolicy

echo "Adding VPN Service CompanyA"
neutron vpn-service-create --name companyAvpn --description "This VPN is to communicate between Proxy server and intermediate server" R-CompAproxy CompanyAproxyserverNetwork

echo "Adding IPSec Site Connections for CompanyA"
neutron ipsec-site-connection-create --name vpnconnection --vpnservice-id companyAvpn --ikepolicy-id companyAikepolicy --ipsecpolicy-id companyAipsecpolicy --peer-address 180.180.180.6 --peer-id 180.180.180.6 --peer-cidr 40.0.0.0/24 --psk opensesame

#Confguration Specific to CompanyB

#@author: Sikandar Khan

echo "Openrc CompanyB"
. ./openrc CompanyB CompanyB

echo "Creating networks in CompanyB" 
echo "Launching 20.0.0.0/24 network in companyB"
neutron net-create CompanyBwebserverNetwork --tenant_id $(keystone tenant-list | grep '\sCompanyB' | awk '{print $2}')
neutron subnet-create CompanyBwebserverNetwork 20.0.0.0/24 --name CompanyBwebserverNetwork

echo "Creating routers on CompanyB"
neutron router-create R-CompBwebServer

echo "Adding Pubic Gateway for R-CompBwebServer public"
neutron router-gateway-set R-CompBwebServer public

echo "Attaching interface of R-CompBwebServer to network CompanyBwebserverNetwork"
neutron router-interface-add R-CompBwebServer $(neutron subnet-list | grep CompanyBwebserverNetwork | awk '{print $2}')

echo "Exporting image" 
export IMAGE=TinyCore

echo "Launching instances in CompanyB" 
nova boot --flavor m1.tiny --image $(nova image-list | grep $IMAGE'\s' | awk '{print $2}') --nic net-id=$(neutron net-list | grep CompanyBwebserverNetwork | awk '{print $2}') CB-Webserver1 --availability_zone=sak:sak
nova boot --flavor m1.tiny --image $(nova image-list | grep $IMAGE'\s' | awk '{print $2}') --nic net-id=$(neutron net-list | grep CompanyBwebserverNetwork | awk '{print $2}') CB-Webserver2 --availability_zone=sak:sak

#Adding Security Rules
echo "Adding Security Rules for CompanyB"

echo "Adding ICMP Rule for CompanyB"
nova secgroup-add-rule default icmp -1 -1 0.0.0.0/0

echo "Adding TCP Rule for CompanyB"
nova secgroup-add-rule default tcp 1 65535 0.0.0.0/0

#Load Balancer for CompanyB
echo "Creating Load Balancing Pool for CompanyB"
neutron lb-pool-create --lb-method ROUND_ROBIN --name companyBpool --protocol HTTP --subnet-id $(neutron subnet-list | grep CompanyBwebserverNetwork | awk '{print $2}')

echo "Creating WebServer's to the pool"
neutron lb-member-create --address  $(nova list | grep CB-Webserver1 | awk '{print $12}' | cut -d "=" -f 2) --protocol-port 80 companyBpool
neutron lb-member-create --address  $(nova list | grep CB-Webserver2 | awk '{print $12}' | cut -d "=" -f 2) --protocol-port 80 companyBpool

echo "Assigning VIP to the Load Balancer of the CompanyB"
neutron lb-vip-create --name companyBvip --protocol-port 80 --protocol HTTP --subnet-id $(neutron subnet-list | grep CompanyBwebserverNetwork | awk '{print $2}') companyBpool

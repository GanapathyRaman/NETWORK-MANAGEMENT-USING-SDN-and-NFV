ODL_REST_Client

===Configure===
Open conf.py to set the IP,Username,Password of your OpenDaylight

===Check System===
Before start, run the following code to check if you systems is ready for the client.
python System_Test.py

If you can see the congratulations info in your computer, it means your system is ready, otherwise please install the missing component before you start the client.

===Using CLI client===
Step 0:Sart ODL and Mininet
Step 1. Disable the flooding in ODL.(if you want)
		python add_drop.py

Step 2. Add primary flows
		python flow_adder.py
Step 3. Start redundancy service
		python Run.py -r
Step 4. Start load balancer service
	python Run.py ¨Cl
Step 5. Start Bothe Load balancer and redundancy service
	python Run.py ¨Ca
Step 6. Sometimes, you want to delete all the flows and start from the beginning, run the following command to remove all flows (primary and secondary flows, except the flows disable the flooding) 
	python flow_deleter.py

===Using GUI client===
python Run_GUI.py
the other steps are same as CLI client




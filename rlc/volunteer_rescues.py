import csv
import pandas as pd
from send_email2 import send_mail

### Definitions
filename = "/Users/ron_two/Documents/projects/RLC/june2018_poundsrescued.csv"

total_pounds = 0
total_events = 0
threshold_pounds = 10

#Empty dict to hold all volunteers & rescue data
rescues = {}
rescues_email = {}

with open(filename, 'r') as data:
	rescues_data = csv.reader(data)
	# [0] 'full_name'
	# [1] 'email'
	# [2] 'phone_number'
	# [3] 'region_name'
	# [4] 'event_title'
	# [5] 'starting_time'
	# [6] 'sum_of_pounds'
	next(rescues_data)

	for row in rescues_data:
		volunteer, email, pounds, num_events = row[0], row[1], row[6], 1
		rescue_obj = {'name': volunteer, 'email': email, 'total pounds': int(pounds), 'total events': 1} 

		#If 'volunteer' is stored as a key in 'rescues', add 'pounds' and increment 'total events' by 1
		if email in rescues.keys():
			rescues[email]['total pounds'] += int(pounds)
			rescues[email]['total events'] += 1
		else:
			rescues[email] = rescue_obj


for volunteer in rescues:
	#Calculate total pounds rescued and total events in month
	total_pounds += rescues[volunteer]['total pounds']
	total_events += rescues[volunteer]['total events']
	#Demarcate volunteers below threshold
	if rescues[volunteer]['total pounds'] > threshold_pounds:
		rescues[volunteer]['send_email'] = 'y'
	else:
		rescues[volunteer]['send_email'] = 'n'

	if rescues[volunteer]['send_email'] == 'y':
		rescues_email[volunteer] = rescues[volunteer]

active_volunteers = len(rescues.keys())
email_volunteers = len(rescues_email.keys())

#Print Results
print("Total Pounds Rescued: "+str(total_pounds))
print("Total Events: "+str(total_events))
print("Total Active Volunteers: "+str(active_volunteers))
print("Total Volunteers to Email: "+str(email_volunteers))

#Login info
send_from = 'email1'


#Store recipient info
recipient = 'email2'
full_name = rescues_email[recipient]['name'].split()
recipient_name = full_name[0]
recipient_pounds = rescues_email[recipient]['total pounds']
recipient_events = rescues_email[recipient]['total events']
recipient_meals = int(recipient_pounds/1.2)

greeting1 = "%s, We thought it might be interesting for you to see the impact your work with Rescuing Leftover Cuisine 
had on your community. Below is the amount of food you saved & meals you served in June due to your commitment to help 
fight hunger:" % recipient_name

greeting2 = "\nYou rescued %i pounds of food in June across %i events. This provided %i meals for the 
food insecure of NYC!" % (recipient_pounds, recipient_events, recipient_meals)

stats = "\nWe rescued a total of %i pounds of food in June (%i meals). Thanks for being a part of the mission 
to end food waste!" % (total_pounds, int(total_pounds/1.2))

message = "Subject: Your June 2018 Impact Report\nHello "+greeting1+greeting2+stats

print("Sending email to %s" % recipient)
password = input('password? ')
email_status = send_mail(send_from, password, recipient, message)

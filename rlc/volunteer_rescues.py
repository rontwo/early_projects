import csv
from rescues_methods import send_mail
from dateutil.relativedelta import relativedelta
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

### Definitions
filename = "CSV_FILEPATH"
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

# #Print Results
# print("Total Pounds Rescued: "+str(total_pounds))
# print("Total Events: "+str(total_events))
# print("Total Active Volunteers: "+str(active_volunteers))
# print("Total Volunteers to Email: "+str(email_volunteers))

#Login info
send_from = input('Enter email: ')
password = input('Enter password: ')

#Create list of all active volunteers to email (above threshold)
send_to = []
for volunteer in rescues_email:
	recipients_full.append(send_to)


#Non-personalized email text
last_month = date.today() - relativedelta(months=1)
greeting1 = '''We thought it might be interesting for you to see the impact your work with Rescuing Leftover 
Cuisine had on your community. Below is the amount of food saved in {d} due to your 
commitment to help fight hunger:'''.format(d=last_month.strftime("%B"))
img_src = "https://raw.githubusercontent.com/rontwo/early_projects/master/rlc/RLC_Rescues.png"

#Send email to all active volunteers above threshold
for recipient in send_to:
	full_name = rescues_email[recipient]['name'].split()
	recipient_name = full_name[0]
	recipient_pounds = rescues_email[recipient]['total pounds']
	recipient_events = rescues_email[recipient]['total events']
	recipient_meals = int(recipient_pounds/1.2)

	#Create Message
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Your {d} Impact Report".format(d=last_month.strftime("%B %Y"))
	msg['From'] = send_from
	msg['To'] = recipient

	#Personalized e-mail body
	header1 = "Hello {}!".format(recipient_name)
	body1 = '''\nYou rescued {:,d} pounds of food in {d} across {} events. This provided {:,d} meals for the
	food insecure of NYC!'''.format(recipient_pounds, d=last_month.strftime("%B"), recipient_events, recipient_meals)
	body2 = "\nRLC, as a whole, rescued a total of {:,d} pounds of food in {} ({:,d} meals).".format(total_pounds, last_month.strftime("%B"), int(total_pounds/1.2))
	signoff = "Thanks for your contribution and being a part of the mission to end food waste!"

	html = """\
	<html>
	  <head></head>
	  <body>
	    <h1>{header1}</h1>
	    <p>
		   {greeting1}<br>
	    </p>
		<table height = "400" width="400" border="0" cellspacing="0" cellpadding="0">
		                <tbody>
		                  <tr>
		                    <td background="{img_src}" style="background-repeat: no-repeat;" bgcolor="#ddf3e9" width="400" height="400" align="center" valign="center" class="bgresize>

		<!--[if gte mso 9]>
		  <v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width:400px;height:400px;">
		    <v:fill type="tile" size="100%,100%" src="{img_src}" color="#ddf3e9" />
		    <v:textbox inset="0,0,0,0">
		  <![endif]-->

		                      <div>
		                        <table width="400" border="0" cellspacing="0" cellpadding="0">
		                          <tbody>
		                            <tr>
		                              <td width="30" align="left" valign="top" style="font-size: 0%;" class="mobile-hidden"><img src="Spacer.gif" width="30" height="1" style="display: block;" border="0"/></td>
		                              <td align="left" valign="top" class="mobile-padding"><table width="100%" border="0" cellspacing="0" cellpadding="0">
		                                  <tbody>
		                                    <tr>
		                                      <td align="center" valign="center" style="padding-top: 95px;" class="padding65">
		                                      <span class="banner-heading55">
		                                      <b>{body1}</b>
		                                      <br><br><b>{body2}</b>
		                                      </span>
		                                      </td>
		                                    </tr>
		                                  </tbody>
		                                </table></td>
		                              <td width="30" align="left" valign="top" class="mobile-hidden" style="font-size: 0%;"><img src="Spacer.gif" width="30" height="1" style="display: block;" border="0"/></td>
		                            </tr>
		                          </tbody>
		                        </table>
		                      </div>

		                      <!--[if gte mso 9]>
		    </v:textbox>
		  </v:rect>
		  <![endif]-->

		                  </td>
		                  </tr>
		                </tbody>
		              </table>
		<br>{signoff}
	  </body>
	</html>
	""".format(**locals())

	#.format(**locals()) searches for local variables to complete string substitution
	msg.attach(MIMEText(html, 'html'))

	print("Sending email to %s" % recipient)
	email_status = send_mail(send_from, password, recipient, msg.as_string())

#Thanks to all volunteers donating their time to a great cause!
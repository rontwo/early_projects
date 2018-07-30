import csv
from rescues_methods import send_mail
from dateutil.relativedelta import relativedelta
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

### Definitions
filename = "CSV_FILENAME"

#Empty dict to hold all volunteers & rescue data
signups = {}

with open(filename, 'r') as data:
	signup_data = csv.reader(data)
	
	### Print header data
	# for row, value in enumerate(next(rescues_data),0):
	# 	print(row, value)
	# 0 id
	# 1 full_name
	# 2 email
	# 3 username
	# 4 phone_number
	# 5 signup_date
	# 6 address
	# 7 organization_name
	# 8 occupation
	# 9 delivery_tool
	# 10 is_under_18
	# 11 lead_rescuer_interest
	# 12 text_notification
	# 13 referral_source
	# 14 last_signin
	# 15 preferred_location_name
	# availabilities....
	next(signup_data)
	
	#Store all volunteers into 'rescues' dict
	for row in signup_data:
		if row[11] == 'true':
			row[11] = True
		else:
			row[11] = False
		full_name, email, signup_date, preferred_location, LR = row[1], row[2], datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S"), row[15], row[11]
		signup_obj = {'name': full_name, 'email': email, 'signup_date': signup_date.strftime("%m/%d/%Y %H:%M:%S"), 'preferred location': preferred_location, 'LR_interest': LR}

		signups[email] = signup_obj

print(signups)
today = datetime.today().strftime("%B %d,%Y")
total_signups = len(signups.keys())

#Print Results
print(f"Total Signups ({today}): "+str(total_signups))

LR_email = []
reg_email = []

for row in signups:
	if signups[row]['LR_interest']:
		LR_email.append(row)
	else:
		reg_email.append(row)

print(LR_email)
print(reg_email)

#Login info
send_from = input('Enter email: ')
password = input('Enter password: ')

#Non-personalized email text
LR_greeting = '''FILL IN'''
reg_greeting = '''FILL IN'''

#Send email to all active volunteers above threshold
for recipient in signups:
	full_name = signups[recipient]['name'].split()
	recipient_name = full_name[0]

	#Create Message
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "FILL IN"
	msg['From'] = send_from
	msg['To'] = recipient

	#Personalized email text
	header1 = "Hello {}!".format(recipient_name)
	
	#HTML for LR email
	html_LR = f"""\
	<html>
	  <head></head>
	  <body>
	    <h1>{header1}</h1>
	    <p>
		   {LR_greeting}<br>
	    </p>
	  </body>
	</html>
	"""

	html_reg = f"""\
	<html>
	  <head></head>
	  <body>
	    <h1>{header1}</h1>
	    <p>
		   {reg_greeting}<br>
	    </p>
	  </body>
	</html>
	"""
	if recipient in LR_greeting:
		msg.attach(MIMEText(html_LR, 'html'))
	else:
		msg.attach(MIMEText(html_reg, 'html'))

	print("Sending email to %s" % recipient)
	email_status = send_mail(send_from, password, recipient, msg.as_string())
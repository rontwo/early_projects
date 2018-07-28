import smtplib

#Create smtp object on port 587 (TLS)
def send_mail(email, password, recipients, message):
	s_obj = smtplib.SMTP('smtp.gmail.com',587)
	s_obj.ehlo()
	s_obj.starttls()
	s_obj.login(email, password)
	s_obj.sendmail(email, recipients, message)
	s_obj.quit()

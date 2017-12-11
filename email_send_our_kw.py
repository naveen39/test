#**************************************method to send Email **********************************************
#**************************************************************************************************************
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import rds_config_our_kw

from error_handling_our_kw import error_handling

mail_user=rds_config_our_kw.mail_user
mail_pwd=rds_config_our_kw.mail_pwd

def email_send(program_name):
     try:
          fromaddr = mail_user
          recipients = ['bnaveen@dhruvsoft.com', 'ramanji@dhruvsoft.com']
          toaddr = "naveensfdc9@gmail.com"
          msg = MIMEMultipart()
          msg['From'] = fromaddr
          msg['To'] = toaddr
          msg['Subject'] = "AWS ZOHO Integration by Python !"+program_name
          
          body = "This mail recieved regading "+program_name+".py exception \n because "
          body=body+str(error_handling())
          msg.attach(MIMEText(body, 'plain'))
          server = smtplib.SMTP('smtp.gmail.com', 587)
          server.starttls()
          server.login(fromaddr, mail_pwd)
          text = msg.as_string()
          server.sendmail(fromaddr, toaddr, text)
          server.quit()
     except Exception as e:
        print(program_name," failed to send mail",e)

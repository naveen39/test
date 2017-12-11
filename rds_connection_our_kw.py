import rds_config_our_kw
from email_send_our_kw import email_send

import pymysql


#******************* AWS RDS CONFIGURATION ***********************************************
#********************************************************************************************************

host='peopleorginstance.cprntwdvlp7k.us-east-1.rds.amazonaws.com'
dbName=rds_config_our_kw.db_name
uname=rds_config_our_kw.db_username
upwd=rds_config_our_kw.db_password
mail_user=rds_config_our_kw.mail_user
mail_pwd=rds_config_our_kw.mail_pwd

#********************** AWS RDS Connection Establisation ****************************************
try:
    #charset='utf8'
    conn = pymysql.connect(host=host,database=dbName, user=uname, password=upwd,charset='utf8')
    print('\n********************** AWS RDS Connection Establisation ****************************************\n')
except Exception as e:
    email_send('***RDS_CONFIGURATION')
    print(e)

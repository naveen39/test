import requests

import json
from json import dumps
import os, datetime, time

# sandbox coach id = 2034239000000171647   product coach id = 2108750000003455240
import rds_config_our_kw
from rds_connection_our_kw import conn

import os, sys,errno
#reload(sys)
#sys.setdefaultencoding('utf-8')

from email_send_our_kw import email_send
from error_handling_our_kw import error_handling
from pprint import pprint
mydir_name=os.path.join(os.getcwd()+'/logs/'+datetime.datetime.now().strftime('%Y-%m-%d'),'latest_coachin_pro_updates')
print(mydir_name)
try:
    os.makedirs(mydir_name)
    print('mydir_name', str(datetime.datetime.now().strftime('%Y-%m-%d')))
except OSError as e:
    if e.errno == 17:  # errno.EEXIST
        os.chmod(mydir_name, 777)

    if e.errno != errno.EEXIST:
        raise   #This was not a "directory exist" error..'
    

filename='coaching_pro_updates '+str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))+'.txt'
#filename="COntactest.txt"
#module='Contacts'
table_name='chargify_subscriptions_table'

kwuid_list=[]
email_list=[]

ratetime=0
coaching_prog_data=''

pro_zohoid=''
pro_name=''
sub_id=''
signup_date=''
pro_Service_Line=''
pro_Mastery_Category=''
pro_Price=''
pro_number=''
pro_Interval=''
pro_rec_price=''
full_name=''
pro_Pay_Rate=''
hold_date=''
cancle_date=''
previous_coach_id=''
chargify_kwuid=''
chargify_email=''
chargify_phone=''
chargify_product_name=''
con_zohoid=''
con_data=''
ac_status=''
pro_mastery_id=''
Hold_Date_Checked=False
update_contact_data=''
coach_pro_namechangeflag_check=''
Signup_Email=''
Signup_Phone=''
kwuid_value=''
who_pays=''
existed_cp_product_id=''
def sub_start():
    print('\n\n*******************************************************contact process started************************************\n\n')

# ****************************start process************************************************************
def sub_handler():
    print('******************************************************contact_handler called************************************\n')
    global mydir_name
    global filename
    global ratetime
    global module
    global table_name,update_contact_data,existed_cp_product_id
    global pro_zohoid,ac_status,pro_mastery_id,Hold_Date_Checked,coach_pro_namechangeflag_check,who_pays,Signup_Email,kwuid_value
    global coaching_prog_data,subid,pro_number,hold_date,cancle_date,chargify_kwuid,chargify_email,con_zohoid,con_data,chargify_product_name,chargify_phone
    global pro_name,No_of_Coaching_Programs,subid,signup_date,pro_Service_Line,pro_Mastery_Category,pro_Price,pro_Interval,pro_rec_price,full_name,pro_Pay_Rate
    
    #print('stared at :',datetime.datetime.now())    
    #print('filename ', filename)
    file=open(os.path.join(mydir_name,filename),'a+')
    file.write("\nRow_ no\t\t\t\t sub_id\t\t\t\t  pro_id \t\t\t  date \t\t\t zoho_id\t\t\t\t insert \t\t\t\t update \n")
    file.close()
        #******************get the date upto to processed or Pagination based on records in the table****************************************************
    contact_cur = conn.cursor()
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * processing records by pages and page limit is 30 coz of 1 min limitation in zoho * * * * * * * * * * * * * * * * * * * * * * * * * *
    quer = "SELECT  First_Name , Last_Name , Primary_Phone , Contact_Type , Email , Signup_Phone , Signup_Email ,\
                                               Chargify_Customer_Id ,Mailing_Street , Mailing_City , Mailing_State , Mailing_Zip , Mailing_Country ,\
                                              Other_Street , Other_City , Other_State , Other_Zip , Other_Country ,Potential_Name , Account_Status , \
                                               Credit_Cart_First_Name , Credit_Card_Last_Name , \
                                              Credit_Card_Billing_Address_1 , Credit_Card_Billing_Address_2 , Credit_Card_Billing_City ,\
                                              Credit_Card_Billing_State , Credit_Card_Billing_Zip , Credit_Card_Billing_Country , CC_ACH , \
                                              Mastery_Product_Id,Recurring_Price , Recurring_Interval_Unit ,Recurring_Interval ,\
                                              Subscription_Id, Contract_End_Date , Renewal_Date ,Stage , Subscription_Link ,  Price ,  Closing_Date ,\
                                              Signup_Date ,    Contract_Start_Date ,Next_Billing_Date ,Coupon , KWUID , Associate_ID ,\
                                              Start_Month , Already_MAPS_Mastery_Coaching_Client_or_ISA_Client , Opt_In_for_Text_Messaging ,\
                                              Referred_By , Region , Sales_Person , MAPS_Customer_No ,  \
                                              Chargify_Notes , No_of_Transactions_Last_Year ,\
                                              No_of_Transactions_This_Year_YTD , Anything_else_to_share_with_your_Coach_Assgn_Team , Average_Sales_Price , \
                                              Do_you_have_a_PC_Program_PCP_in_your_MC,Do_you_have_or_Are_you_on_a_team_and_what_is_the_role , Do_you_prospect , \
                                               How_long_have_you_been_in_the_PC_Role , How_long_have_you_been_in_this_role , How_long_have_you_been_with_KW, \
                                              How_many_agents_in_your_Market_Center,Rating_for_Skill_in_Using_Growth_Initiative_Tools ,Market_Center_Chargify,\
                                              Role_To_Be_Coached_In, Secondary_Name, Size_of_Team ,   Transactions_Goal_for_this_Year , \
                                              What_is_the_No1_goal_for_joining_the_MAPS_coaching , who_pays,Navison_CMP_No,reference,status,sub_canceled_at,sub_updated_at,\
                                              sub_expires_at,processed_day,product_Name,ISA_Salesperson,top_producer_contact_id,organization_contact_firstname,\
                                              organization_contact_lastname FROM \
                                              " + table_name+" where  Subscription_Id=16443893 ORDER BY modified_date  ASC limit 1500"
                    #charg cust id 7
                    # opp name col 18
                    #product_id 29
                    #sub_id 33
                    #kwuid 44   referred_by 42  role_associated_with_contract  44  no_of_transactions_last_year 48 average_sales_price 51
                    #email 4 how_long_have_you_been_in_the_pc_role 55 market_center 60 secondary_name 66 status 70
    # ************************ check the kwuid , sub id, pro id field numbers*********************************
    #print(quer)
    contact_cur.execute(quer)
    for r, field in enumerate(contact_cur):
        print(r)
        def f(field):
            if str(field) is not None and str(field)!='None':
                if str(field)!='None':
                    return field
                else:
                    return ''
            else:
                return ''
            
        Hold_Date_Checked=False
        coach_pro_namechangeflag_check=''
        kwuid_value=''
        who_pays=''
        who_pays=str(f(field[72]))
        print('who_pays    ',who_pays)
        Signup_Email=''
        Signup_Email=str(f(field[6])).replace('&','%26')
        Signup_Phone=''
        Signup_Phone=str(f(field[2]))
        pro_zohoid=''
        ac_status=''
        pro_mastery_id=''
        pro_name=''
        subid=''
        signup_date=''
        pro_Service_Line=''
        pro_Mastery_Category=''
        pro_Price=''
        pro_number=''
        coaching_prog_data=''
        pro_Interval=''
        pro_rec_price=''
        chargify_kwuid=''
        chargify_email=''
        chargify_phone=''
        chargify_product_name=''
        con_zohoid=''
        con_data=''
        update_contact_data=''
        chargify_kwuid=str(f(field[44]))
        chargify_email=str(f(field[4]))
        chargify_phone=str(f(field[2]))
        full_name= str(f(field[0])) +' '+ str(f(field[1])) +' '
        pro_Pay_Rate=''
        previous_coach_id=''
        today=str((datetime.datetime.now()-datetime.timedelta(0)).strftime('%Y-%m-%d'))
        cancle_date=''
        chargify_product_name=str(f(field[80]))
        existed_cp_product_id=''
        print(today)
        if str(f(field[19]))=='active':
            ac_status='Active'
        if str(f(field[19]))=='past_due':
            ac_status='Past Due'
        if str(f(field[19]))=='canceled':
            ac_status='Cancelled'
            
            cancle_d=datetime.datetime.strptime(str(f(field[76])), "%Y-%m-%d %H:%M:%S.%f")
            cancle_date=cancle_d.date()
        

        if str(f(field[19]))=='unpaid':
            ac_status='Unpaid'
        if str(f(field[19]))=='expired':
            ac_status='Expired'
            cancle_date=str(f(field[78]))
        if str(f(field[35]))!='':
            renewal_d=datetime.datetime.strptime(str(f(field[35])), "%Y-%m-%d %H:%M:%S.%f")
            renewal_date=renewal_d.date()
        else:
            renewal_date=str(f(field[35]))
        

        if str(f(field[40]))!='':
            
            signup_d=datetime.datetime.strptime(str(f(field[40])), "%Y-%m-%d %H:%M:%S.%f")
            signup_date_field=signup_d.date()
            print(str(signup_date_field))
            signup_date_list=str(signup_date_field).split('-')
            print(signup_date_list)
            signup_date=signup_date_list[1]+'-'+signup_date_list[2]+'-'+signup_date_list[0]
            print(str(signup_date))
        else:
            signup_date=str(f(field[40]))
            signup_date_field=str(f(field[40]))

        
        file =open(os.path.join(mydir_name,filename),'a+')
        file.write("\n " + str(r + 1) + '\t\t' + str(f(field[33])) + '\t\t\t\t'+  str(f(field[29])))
        file.close()
        
        if chargify_kwuid=='0':
            kwuid_value=''
        else:
            kwuid_value=chargify_kwuid

        #********************contact field maps for creation of changed contact******************************************
            
        con_data='<Contacts>' + '<row no=\"' + str(1) + '\">' + '<FL val=\"First Name\">' + str(f(field[0])) + '</FL\
                                  >' + '<FL val=\"Last Name\">' + str(f(field[1])) + '</FL\
                                    >' + '<FL val=\"Contact Type\">' + str(f(field[3])) + '</FL\
				 >' + '<FL val=\"Primary Phone\">' + str(f(field[2])) + '</FL\
				 >' + '<FL val=\"Signup Phone\">' + str(f(field[2])) + '</FL\
                                >' + '<FL val=\"Email\">' + str(f(field[4])) + '</FL\
				 >' + '<FL val=\"Signup Email\">' + str(f(field[6])) + '</FL\
				 >' + '<FL val=\"KWUID\">' + str(kwuid_value)+ '</FL\
				 >' + '<FL val=\"Chargify Customer Id\">' + str(f(field[7])) + '</FL\
				 >' + '<FL val=\"Mailing Street\">' + str(f(field[8])) + '</FL\
                               >' + '<FL val=\"Mailing City\">' + str(f(field[9])) + '</FL\
                                >' + '<FL val=\"Mailing State\">' + str(f(field[10])) + '</FL\
                                >' + '<FL val=\"Mailing Zip\">' + str(f(field[11])) + '</FL\
                                >' + '<FL val=\"Mailing Country\">' + str(f(field[12])) + '</FL\
				 >' + '<FL val=\"Other Street\">' + str(f(field[13])) + '</FL\
				 >' + '<FL val=\"Other City\">' + str(f(field[14])) + '</FL\
				 >' + '<FL val=\"Other State\">' + str(f(field[15])) + '</FL\
				 >' + '<FL val=\"Other Zip\">' + str(f(field[16])) + '</FL\
                                  >' + '<FL val=\"Other Country\">' + str(f(field[17])) + '</FL\
				 >' + '<FL val=\"Associate ID\">' + str(f(field[45])) + '</FL></row>' + '</Contacts>'

        update_contact_data='<Contacts>' + '<row no=\"' + str(1) + '\">' + '<FL val=\"Signup Phone\">' + str(f(field[2])) + '</FL\
                                     >' + '<FL val=\"Signup Email\">' + str(f(field[6])) + '</FL\
                                     >' + '<FL val=\"Chargify Customer Id\">' + str(f(field[7])) + '</FL></row>' + '</Contacts>'




        #*******************coaching program field mapping *****************************************

            
        coaching_prog_data=coaching_prog_data+'<CustomModule9>' + '<row no=\"' + str(1) + '\">' + '<FL val=\"Credit Cart First Name\">' + str(f(field[20])).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Credit Card Last Name\">' + str(f(field[21])).replace('&','%26') + '</FL\
                                 >' + '<FL val=\"Credit Card Billing Address 1\">' + str(f(field[22])).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Credit Card Billing Address 2\">' + str(f(field[23])).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Credit Card Billing City\">' + str(f(field[24])).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Credit Card Billing State\">' + str(f(field[25])).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Credit Card Billing Zip\">' + str(f(field[26])).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Credit Card Billing Country\">' + str(f(field[27])).replace('&','%26') + '</FL\
                                 >' + '<FL val=\"CC/ACH\">' + str(f(field[28])) + '</FL\
                                 >' + '<FL val=\"Chargify Customer Id\">' + str(f(field[7])) + '</FL\
                                >' + '<FL val=\"Signup Date\">' + str(signup_date_field) + '</FL\
				>' + '<FL val=\"Price\">' + str(f(field[38])/100) + '</FL\
				>' + '<FL val=\"Product ID\">' + str(f(field[29])) + '</FL\
                                 >' + '<FL val=\"Recurring Interval\">' + str(f(field[32])) + '</FL\
                                 >' + '<FL val=\"Recurring Interval Unit\">' + str(f(field[31])) + '</FL\
                                  >' + '<FL val=\"Recurring Price\">' + str(f(field[30])/100)  + '</FL\
				 >' + '<FL val=\"Account Status\">' + str(ac_status).replace('&','%26') + '</FL\
                                >' + '<FL val=\"Renewal Date\">' +  str(renewal_date)  + '</FL\
				>' + '<FL val=\"Updated from AWS\">' + str((datetime.datetime.now()-datetime.timedelta(0)).strftime('%Y-%m-%d'))+ '</FL\
                                 >' + '<FL val=\"Start Month\">' + str(f(field[46])).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Already MAPS Mastery Coaching Client or ISA Client\">' + str(f(field[47])).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Opt-In for Text Messaging\">' + str(f(field[48])).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Referred By\">' + str(f(field[49])).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Region\">' + str(f(field[50])).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Sales Person\">' + str(f(field[51])).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Secondary Name\">' + str(f(field[68])).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Chargify Notes\">' + str(f(field[53])).replace('&','%26') + '</FL\
                                 >' + '<FL val=\"No of Transactions Last Year\">' + str(f(field[54])).replace('&','%26') + '</FL\
				 >' + '<FL val=\"No of Transactions This Year (YTD)\">' + str(f(field[55])).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Anything else to share with your Coach Assgn Team\">' + str(f(field[56])).replace('&','%26')+ '</FL\
                                 >' + '<FL val=\"Average Sales Price\">' + str(f(field[57])).replace('&','%26') + '</FL\
                                 >' + '<FL val=\"Do you have a PC Program (PCP) in your MC?\">' + str(f(field[58])).replace('&','%26') + '</FL\
                                 >' + '<FL val=\"Do you have/Are you on a team and what is the role\">' + str(f(field[59])).replace('&','%26') + '</FL\
                                 >' + '<FL val=\"Do you prospect?\">' + str(f(field[60])).replace('&','%26') + '</FL\
                                 >' + '<FL val=\"How long have you been in the PC Role?\"><![CDATA[' + str(f(field[61])) + ']]></FL\
                                 >' + '<FL val=\"How long have you been in this role?\"><![CDATA[' + str(f(field[62])) + ']]></FL\
                                 >' + '<FL val=\"How long have you been with KW?\"><![CDATA[' + str(f(field[63])) + ']]></FL\
                                 >' + '<FL val=\"How many agents in your Market Center?\">' + str(f(field[64])).replace('&','%26') + '</FL\
                                 >' + '<FL val=\"Rating for Skill in Using Growth Initiative Tools\">' + str(f(field[65])).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Market Center_Chargify\">' + str(f(field[66])).replace('&','%26') + '</FL\
                                  >' + '<FL val=\"Role To Be Coached In\">' + str(f(field[67])).replace('&','%26') + '</FL\
                                  >' + '<FL val=\"Size of Team\">' + str(f(field[69])).replace('&','%26') + '</FL\
                                  >' + '<FL val=\"MAPS Customer No\">' + str(f(field[52])).replace('&','%26') + '</FL\
				>' + '<FL val=\"Transactions Goal for this Year\">' + str(f(field[70])).replace('&','%26') + '</FL\
                               >' + '<FL val=\"What is the No1 goal for joining the MAPS coaching\">' + str(f(field[71])).replace('&','%26') + '</FL\
                                >' + '<FL val=\"Who Pays?\">' + str(f(field[72])).replace('&','%26') + '</FL\
                                >' + '<FL val=\"AWS Update Status\">' + str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')) + '</FL\
                                >' + '<FL val=\"Cancelled Date\">' + str(cancle_date) + '</FL\
                                 >' + '<FL val=\"ISA Salesperson\">' + str(f(field[81])).replace('&',' ') + '</FL\
                                >' + '<FL val=\"Top Producer Contact ID\">' + str(f(field[82])).replace('&',' ') + '</FL\
                                >' + '<FL val=\"Navison CMP No\">' + str(f(field[73])).replace('&','%26') + '</FL>'
                                                                       
                                                

                                                                       
        print('pro id', str(f(field[29])))
        
        
        pro_number=str(f(field[29]))
        if str(f(field[40]))!='':
            d=datetime.datetime.strptime(str(f(field[40])), "%Y-%m-%d %H:%M:%S.%f")
            signup_date_field=signup_d.date()
            print(str(signup_date_field))
            signup_date_list=str(signup_date_field).split('-')
            print(signup_date_list)
            signup_date=signup_date_list[1]+'-'+signup_date_list[2]+'-'+signup_date_list[0]
            print(str(signup_date))
        else:
            signup_date=str(f(field[40]))
            signup_date_field=str(f(field[40]))
        print(str(f(field[77])))
        if str(f(field[77]))!='':

            hold_d=datetime.datetime.strptime(str(f(field[77])), "%Y-%m-%d %H:%M:%S.%f")
            hold_date=hold_d.date()
        else:
            hold_date=''

        subid= str(f(field[33]))
        #product_search( str(f(field[29])),'Products','Mastery Product ID')
        if ratetime>55:
            time.sleep(20)
            ratetime=0
        
       
        #_______________________________________________________________________________________________________________________________
            
        #************  coaching_program_search for CP is exsited  or not ************************************************
        #_______________________________________________________________________________________________________________________________
        
        Other_Department=[17302818,17306014,17307301,17300093,17305443]    
        if int(subid) not in Other_Department:
            coaching_program_search(subid,'CustomModule9','Subscription Id')
        else:
            print('\n ***************________Subscription id = ',subid, '_______is belongs to Other Department ')

#_______________________________________________________________________________________________________________________________

#************  product_search for Product is exsited  or not ************************************************
#_______________________________________________________________________________________________________________________________


def product_search(field_name,module,field_label):
    global mydir_name
    global filename
    global ratetime
    
    global table_name
    global pro_zohoid,update_contact_data
    global coaching_prog_data,subid,pro_number,hold_date,cancle_date,chargify_product_name,ac_status,pro_mastery_id
    global pro_name,No_of_Coaching_Programs,subid,signup_date,pro_Service_Line,pro_Mastery_Category,pro_Price,pro_Interval,pro_rec_price,full_name,pro_Pay_Rate,previous_coach_id
    
    #print('entered to search ',field_name,field_label)
    authtoken='5f7af2d8ffc3345c6b0228c1e3ed135c'
    #xmlData=con_data
    print('\n ****in search '+module+' by ' +field_label+'='+field_name+'****\n')
    
    url2="https://crmsandbox.zoho.com/crm/private/json/{}/searchRecords?authtoken=5f7af2d8ffc3345c6b0228c1e3ed135c&scope=crmapi&criteria=({}:{})&fromIndex=1&toIndex=200".format(module,field_label,field_name)
   # print('url2--',url2)
    #print ('dssdsd',data['response'])
    try:
        ac=requests.get(url2)
        #print(ac)
        data=ac.json()
        ratetime=ratetime+1
        #print(data['response'])
        if 'nodata' in data['response']:
            print(data['response']['nodata']['message'])
            print(data['response']['nodata']['message'])
            email_send('--- product_id in product  '+str(field_name)+' of '+str(subid)+' not existed-----production_coaching_pro')
            chargify_product_name_lower=chargify_product_name.lower()
            print(chargify_product_name_lower)
            if 'hold'  in chargify_product_name_lower and ac_status=='Active':
                print('*************hold************',chargify_product_name_lower,'*************************')
                coaching_prog_data=coaching_prog_data + '<FL val=\"Account Status\">' + str('Hold') + '</FL>'
                print('*************hold************',chargify_product_name_lower,'*************************',coaching_prog_data)
            coaching_prog_data=coaching_prog_data+'<FL val=\"Product ID\">' + str(pro_number) + '</FL\
                                                                      >'+ '<FL val=\"Service Line\">' + str(pro_Service_Line) + '</FL\
                                                                      >'+ '<FL val=\"Mastery Category\">' + str(pro_Mastery_Category) + '</FL\
                                                                      >' + '<FL val=\"Price\">' + str(pro_Price) + '</FL\
                                                                     >' + '<FL val=\"Product Name\">' + str(pro_zohoid) + '</FL\
                                                                       >' + '<FL val=\"Pay Rate for Product\">' + str(pro_Pay_Rate) + '</FL>'
            
            

            #pushintozoho(xmlData,kwuid)
            
        if 'result' in data['response']:
            print('\n ****************************pro matched  ')
            if data['response']['result']['Products']['row']:
            #print('\n--- true------------------\n')
            #x=data['response']['result']['Contacts']['row']
                dataType= type(data['response']['result']['Products']['row'])
                #print(dataType,'--dataType is-')
                # *****records alreday exited**************
                if type(data['response']['result']['Products']['row']) is dict:
                    #print(dataType,'--->means single record')
                    #print('single records exist   ')
                    #print(data['response']['result']['Contacts']['row']['FL'][0]['content'])
                    print(type(data['response']['result']['Products']['row']['FL']))
                    pro_dic={}
                    for pro_list in data['response']['result']['Products']['row']['FL']:
                        pro_dic[pro_list['val']]=pro_list['content']

                    #print('pro_dic--->',pro_dic)

                    if field_label in pro_dic.keys():
                            pro_id_value=pro_dic['Mastery Product ID']
                            if pro_id_value==field_name:
                               
                                pro_name=pro_dic['Product Name']
                                print(pro_name)
                                pro_zohoid=pro_dic['PRODUCTID']
                                
                                pro_Service_Line=pro_dic['Service Line']
                                if 'Mastery Category' in pro_dic.keys():
                                    pro_Mastery_Category=pro_dic['Mastery Category']
                                else:
                                    pro_Mastery_Category=''
                                if 'Price' in pro_dic.keys():
                                    pro_Price=pro_dic['Price']
                                else:
                                    pro_Price=''    
                                
                                #pro_Interval=pro_dic['Recurring Interval']
                                #pro_rec_price=pro_dic['Recurring Price']
                                
                                if 'Pay Rate' in pro_dic.keys():
                                    pro_Pay_Rate=pro_dic['Pay Rate']
                                else:
                                    pro_Pay_Rate=''
                                

                elif dataType is list:
                    print(dataType, '---means more than one record')
                    for rec in data['response']['result']['Products']['row']:
                        pro_dic={} 
                        for  pro_field_list  in rec['FL']:
                            pro_dic[pro_field_list['val']]=pro_field_list['content']

                        #print('pro_dic',pro_dic)
                        print(field_label)
                        print('field_label',field_label,field_name)
                        if field_label in pro_dic.keys():
                            pro_id_value=pro_dic['Mastery Product ID']
                            if pro_id_value==field_name:
                                print('pro matched',pro_id_value,field_name)
                                pro_name=pro_dic['Product Name']
                                pro_zohoid=pro_dic['PRODUCTID']
                                pro_Service_Line=pro_dic['Service Line']
                                if 'Mastery Category' in pro_dic.keys():
                                    pro_Mastery_Category=pro_dic['Mastery Category']
                                else:
                                    pro_Mastery_Category=''
                                if 'Price' in pro_dic.keys():
                                    pro_Price=pro_dic['Price']
                                else:
                                    pro_Price=''    
                                
                                #pro_Interval=pro_dic['Recurring Interval']
                                #pro_rec_price=pro_dic['Recurring Price']
                                
                                if 'Pay Rate' in pro_dic.keys():
                                    pro_Pay_Rate=pro_dic['Pay Rate']
                                else:
                                    pro_Pay_Rate=''
                                
                                
                                break
                        else:
                            print('pro not matched',pro_id_value,field_name)
                            
    except Exception as e:
        email_send('---failed at search  of product_id in product  '+str(pro_id_value)+' '+str(e)+'-----production_coaching_pro')
        print(e)

def coaching_program_search(field_name,module,field_label):
    global mydir_name
    global filename
    global ratetime
    
    global table_name
    global pro_zohoid,Hold_Date_Checked,update_contact_data,coach_pro_namechangeflag_check,existed_cp_product_id
    global coaching_prog_data,subid,pro_number,hold_date,cancle_date,chargify_kwuid,chargify_email,con_zohoid,con_data
    global pro_name,No_of_Coaching_Programs,subid,signup_date,pro_Service_Line,pro_Mastery_Category,pro_Price,pro_Interval,pro_rec_price,full_name,pro_Pay_Rate,previous_coach_id
    
    #print('entered to search ',field_name,field_label)
    authtoken='5f7af2d8ffc3345c6b0228c1e3ed135c'
    #xmlData=con_data
    print('\n ****in search '+module+' by ' +field_label+'='+field_name+'****\n')
    
    url2="https://crmsandbox.zoho.com/crm/private/json/{}/searchRecords?authtoken=5f7af2d8ffc3345c6b0228c1e3ed135c&scope=crmapi&criteria=({}:{})&fromIndex=1&toIndex=200".format(module,field_label,field_name)
    print('url2--',url2)
    #print ('dssdsd',data['response'])
    try:
        ac=requests.get(url2)
        #print(ac.json())
        data=ac.json()
        ratetime=ratetime+1
        #print(data['response'])
        if 'nodata' in data['response']:
            
            print(data['response']['nodata'])

            file=open(os.path.join(mydir_name,filename),'a+')
            file.write('\t\t\t'+data['response']['nodata']['message']+'\t\t\t\n')
            file.close()
            #product_search(pro_id,'Products','Mastery Product ID')
            #email_send('---coaching_program_search  failed due to '+data['response']['nodata']['message']+' OF '+str(field_name)+' -----production_coaching_pro')

            
            
            #pushintozoho(xmlData,kwuid)
            
        if 'result' in data['response']:
            print('\n *******************partally **matched  ', field_name)
            if data['response']['result']['CustomModule9']['row']:
            #print('\n--- true------------------\n')
            #x=data['response']['result']['Deals']['row']
                dataType= type(data['response']['result']['CustomModule9']['row'])
                #print(dataType,'--dataType is-')
                # *****records alreday exited**************
                if type(data['response']['result']['CustomModule9']['row']) is dict:
                    print(dataType,'--->means single record')
                    #print('single records exist   ')
                    print(data['response']['result']['CustomModule9']['row']['FL'][0]['content'])
                    coach_dic={}
                    for coach_list in data['response']['result']['CustomModule9']['row']['FL']:
                        coach_dic[coach_list['val']]=coach_list['content']

                    #print('coach_dic-->',coach_dic)
                    print(field_label,coach_dic.keys())
                    if  field_label in coach_dic.keys():
                        coach_value=coach_dic['Subscription Id']
                        print(coach_value)
                        Hold_Date_Checked=coach_dic['Hold Date Checked']
                        print('Hold_Date_Checked',Hold_Date_Checked)
                        if 'Previous Coach_ID' in coach_dic.keys():
                            print(coach_dic['Previous Coach_ID'])
                            previous_coach_id=coach_dic['Previous Coach_ID']
                        else:
                            previous_coach_id=''
                        if coach_value==field_name:
                            print('coach matched',coach_value,field_name)
                            coach_zohoid=coach_dic['CUSTOMMODULE9_ID']
                            if 'Name Change Done' in coach_dic:
                                coach_pro_namechangeflag_check=coach_dic['Name Change Done']
                            else:
                                coach_pro_namechangeflag_check='False'
                            if 'Product ID' in coach_dic:
                                existed_cp_product_id=coach_dic['Product ID']
                            else:
                                existed_cp_product_id=''
                                
                            
                            print(coach_zohoid,coach_pro_namechangeflag_check)
                            product_search( pro_number,'Products','Mastery Product ID')
                            
                            #________________________________________________________________
                            #   Name Change Done is true or not 
                            #________________________________________________________________
                            

                            if (coach_pro_namechangeflag_check=='true' or who_pays.replace(' ','')=='MarketCenter' or who_pays=='Region'):
                                coaching_program_update(coach_zohoid,'CustomModule9',field_name)
                            else:
                                print((chargify_kwuid!='' and chargify_kwuid is not None) and chargify_kwuid!='0')
                                if (chargify_kwuid!='' and chargify_kwuid is not None) and chargify_kwuid!='0':
                                    print('chargify_kwuid',chargify_kwuid)

                                    if 'KWUID' in coach_dic.keys():
                                        print(coach_dic['KWUID'],chargify_kwuid,coach_dic['KWUID']==chargify_kwuid )
                                        if coach_dic['KWUID']==chargify_kwuid:
                                            print(coach_dic['KWUID'],chargify_kwuid)
                                            coaching_program_update(coach_zohoid,'CustomModule9',field_name)
                                        else:
                                            print(' kwuid contact changed')
                                            print(chargify_kwuid,'<---chargify <--KWUID--> existed in CP--->',coach_dic['KWUID'] if 'KWUID' in coach_dic else '' )
                                            
                                            search(chargify_kwuid,'Contacts','KWUID',subid)
                                            coaching_prog_data=coaching_prog_data  + '<FL val=\"Contact Name_ID\">' + str(con_zohoid) + '</FL>'
                                            coaching_program_update(coach_zohoid,'CustomModule9',field_name)
                                    else:
                                        print(' kwuid contact changed')
                                        print(chargify_kwuid,'<---chargify <--EMAIL--> existed in CP--->',coach_dic['KWUID'] if 'KWUID' in coach_dic else '' )
                                        search(chargify_kwuid,'Contacts','KWUID',subid)
                                        coaching_prog_data=coaching_prog_data  + '<FL val=\"Contact Name_ID\">' + str(con_zohoid) + '</FL>'
                                        coaching_program_update(coach_zohoid,'CustomModule9',field_name)
                                        
                                elif chargify_email!='' or chargify_email is not None:
                                    if 'Email' in coach_dic.keys():
                                        print(coach_dic['Email'] ,chargify_email,coach_dic['Email']==chargify_email)
                                        if coach_dic['Email']==chargify_email:
                                            print(coach_dic['Email'] ,chargify_email)
                                            coaching_program_update(coach_zohoid,'CustomModule9',field_name)
                                        else:
                                            print('email contact changed')
                                            print(chargify_email,' <---chargify <--EMAIL--> existed in CP---> ',coach_dic['Email'] if 'Email' in coach_dic else '')
                                            search(chargify_email,'Contacts','Email',subid)
                                            coaching_prog_data=coaching_prog_data  + '<FL val=\"Contact Name_ID\">' + str(con_zohoid) + '</FL>'
                                            coaching_program_update(coach_zohoid,'CustomModule9',field_name)
                                    else:
                                        print(' Email contact changed')
                                        print(chargify_email,'<---chargify <--EMAIL--> existed in CP--->',coach_dic['Email'] if 'Email' in coach_dic else '' )
                                        search(chargify_email,'Contacts','Email',subid)
                                        coaching_prog_data=coaching_prog_data  + '<FL val=\"Contact Name_ID\">' + str(con_zohoid) + '</FL>'
                                        coaching_program_update(coach_zohoid,'CustomModule9',field_name)
                                else:
                                    print('search for changed contact')
                                    if 'KWUID' in coach_dic.keys():
                                        print('*************kwuid exist',coach_dic['KWUID'],'sub id',subid)
                                        coach_kwuid=coach_dic['KWUID']
                                        search(coach_kwuid,'Contacts','KWUID',subid)
                                        coaching_prog_data=coaching_prog_data  + '<FL val=\"Contact Name_ID\">' + str(con_zohoid) + '</FL>'
                                        coaching_program_update(coach_zohoid,'CustomModule9',field_name)
                                    else:
                                        print('\n ****************no kwuid  looking for email*******************')
                                        if 'Email' in coach_dic.keys():
                                            print('email ',coach_dic['Email'])
                                            coach_email=coach_dic['Email']
                                            search(coach_email,'Contacts','Email',subid)
                                            
                                            coaching_prog_data=coaching_prog_data  + '<FL val=\"Contact Name_ID\">' + str(con_zohoid) + '</FL>'
                                            coaching_program_update(coach_zohoid,'CustomModule9',field_name)



                                #coaching_program_update(coach_zohoid,'CustomModule9',field_name)
                    
                    
                elif dataType is list:
                    print(dataType, '---means more than one record')
                    for rec in data['response']['result']['CustomModule9']['row']:
                        
                        coach_dic={}
                        #print('coach_dic',coach_dic)
                        for  coach_field_list  in rec['FL']:
                            coach_dic[coach_field_list['val']]=coach_field_list['content']

                        #print('ac_dic',con_dic)
                        print(field_label)
                        print('field_label',field_label,field_name)
                        if field_label in coach_dic.keys():
                            coach_value=coach_dic['Subscription Id']
                            print(coach_value)
                            Hold_Date_Checked=coach_dic['Hold Date Checked']
                            print('Hold_Date_Checked',Hold_Date_Checked)
                            if 'Previous Coach_ID' in coach_dic.keys():
                                 previous_coach_id=coach_dic['Previous Coach_ID']
                            else:
                                previous_coach_id=''
                            if coach_value==field_name:
                                print('opp matched',coach_value,field_name)
                                coach_zohoid=coach_dic['CUSTOMMODULE9_ID']
                                if 'Name Change Done' in coach_dic:
                                    coach_pro_namechangeflag_check=coach_dic['Name Change Done']
                                else:
                                    coach_pro_namechangeflag_check='False'
                                if 'Product ID' in coach_dic:
                                    existed_cp_product_id=coach_dic['Product ID']
                                else:
                                    existed_cp_product_id=''
                                    
                                print(coach_zohoid,coach_pro_namechangeflag_check,existed_cp_product_id)
                                product_search( pro_number,'Products','Mastery Product ID')

                                #________________________________________________________________
                                #   Name Change Done is true or not
                                #________________________________________________________________

                                if (coach_pro_namechangeflag_check=='true' or who_pays.replace(' ','')=='MarketCenter' or who_pays=='Region'):
                                    coaching_program_update(coach_zohoid,'CustomModule9',field_name)
                                else:
                                    if (chargify_kwuid!='' and chargify_kwuid is not None) and chargify_kwuid!='0':
                                        if 'KWUID' in coach_dic.keys():
                                            print(coach_dic['KWUID'],chargify_kwuid,coach_dic['KWUID']==chargify_kwuid )
                                            if coach_dic['KWUID']==chargify_kwuid:
                                                print(coach_dic['KWUID'],chargify_kwuid)
                                                coaching_program_update(coach_zohoid,'CustomModule9',field_name)
                                            else:
                                                print(' kwuid contact changed')
                                                print(chargify_kwuid,'<---chargify <--KWUID--> existed in CP--->',coach_dic['KWUID'] if 'KWUID' in coach_dic else '' )
                                                search(chargify_kwuid,'Contacts','KWUID',subid)
                                                coaching_prog_data=coaching_prog_data  + '<FL val=\"Contact Name_ID\">' + str(con_zohoid) + '</FL>'
                                                coaching_program_update(coach_zohoid,'CustomModule9',field_name)
                                        else:
                                            print(' kwuid contact changed')
                                            print(chargify_kwuid,'<---chargify <--EMAIL--> existed in CP--->',coach_dic['KWUID'] if 'KWUID' in coach_dic else '' )
                                            search(chargify_kwuid,'Contacts','KWUID',subid)
                                            coaching_prog_data=coaching_prog_data  + '<FL val=\"Contact Name_ID\">' + str(con_zohoid) + '</FL>'
                                            coaching_program_update(coach_zohoid,'CustomModule9',field_name)
                                        
                                    elif chargify_email!='' or chargify_email is not None:
                                        if 'Email' in coach_dic.keys():
                                            print(coach_dic['Email'] ,chargify_email,coach_dic['Email']==chargify_email)
                                            if coach_dic['Email']==chargify_email:
                                                print(coach_dic['Email'] ,chargify_email)
                                                coaching_program_update(coach_zohoid,'CustomModule9',field_name)
                                            else:
                                                print('email contact changed')
                                                print(chargify_email,' <---chargify <--EMAIL--> existed in CP---> ',coach_dic['Email'] if 'Email' in coach_dic else '')
                                                
                                                search(chargify_email,'Contacts','Email',subid)
                                                coaching_prog_data=coaching_prog_data  + '<FL val=\"Contact Name_ID\">' + str(con_zohoid) + '</FL>'
                                                coaching_program_update(coach_zohoid,'CustomModule9',field_name)
                                        else:
                                            print(' Email contact changed')
                                            print(chargify_email,'<---chargify <--EMAIL--> existed in CP--->',coach_dic['Email'] if 'Email' in coach_dic else '' )
                                            search(chargify_email,'Contacts','Email',subid)
                                            coaching_prog_data=coaching_prog_data  + '<FL val=\"Contact Name_ID\">' + str(con_zohoid) + '</FL>'
                                            coaching_program_update(coach_zohoid,'CustomModule9',field_name)
                                    else:
                                        print('search for changed contact')
                                        if 'KWUID' in coach_dic.keys():
                                            print('*************kwuid exist',coach_dic['KWUID'],'sub id',subid)
                                            coach_kwuid=coach_dic['KWUID']
                                            search(coach_kwuid,'Contacts','KWUID',subid)
                                            coaching_prog_data=coaching_prog_data  + '<FL val=\"Contact Name_ID\">' + str(con_zohoid) + '</FL>'
                                            coaching_program_update(coach_zohoid,'CustomModule9',field_name)
                                        else:
                                            print('\n ****************no kwuid  looking for email*******************')
                                            if 'Email' in coach_dic.keys():
                                                print('email ',coach_dic['Email'])
                                                coach_email=coach_dic['Email']
                                                search(coach_email,'Contacts','Email',subid)
                                                coaching_prog_data=coaching_prog_data  + '<FL val=\"Contact Name_ID\">' + str(con_zohoid) + '</FL>'
                                                coaching_program_update(coach_zohoid,'CustomModule9',field_name)

                                    #coaching_program_update(coach_zohoid,'CustomModule9',field_name)
                                break
                        else:
                            print('coach not matched',field_name)
            
    except Exception as e:
        email_send('---search  of sub_id in coaching prog  '+str(field_name)+'-----production_coaching_pro')
        print(e)


def coaching_program_update(coaching_prog_id,module,field_value):
    global mydir_name
    global filename
    global ratetime
    
    global table_name
    global pro_zohoid,Hold_Date_Checked,coach_pro_namechangeflag_check,Signup_Email,Signup_Phone,kwuid_value,existed_cp_product_id
    global coaching_prog_data,subid,pro_number,hold_date,cancle_date,ac_status,chargify_kwuid,chargify_email,con_zohoid,pro_mastery_id
    global pro_name,subid,signup_date,pro_Service_Line,pro_Mastery_Category,pro_Price,pro_rec_price,full_name,pro_Pay_Rate,previous_coach_id

    print('\n *********************coaching_program_update update ************************************************************\n',pro_name)
    print('coaching_prog_id ,pro_Pay_Rate ',coaching_prog_id,pro_Pay_Rate,pro_name.replace(u"\u2013", " "))
    
    #print('entered to search ',field_name,field_label)
    authtoken='5f7af2d8ffc3345c6b0228c1e3ed135c'
    product_lower=pro_name.lower()
    
    print(product_lower.replace(u"\u2013", " "),'hold' not in product_lower)
    print(' \n existed_cp_product_id ', existed_cp_product_id,' pro_number ',pro_number,'pro_Mastery_Category.lower()',pro_Mastery_Category.lower(),(pro_Mastery_Category.lower()=='group' and existed_cp_product_id!=pro_number))
    if 'hold' not in product_lower.replace(u"\u2013", " "):
        print('*************not hold************',product_lower,pro_Pay_Rate,'*************************')

        print((pro_Mastery_Category.lower()=='group' and existed_cp_product_id!=pro_number)  )
        
        if ((pro_Mastery_Category.lower()=='group' and existed_cp_product_id!=pro_number) ):
            print('*************group************',product_lower,pro_Mastery_Category,'*************************')
            if (coach_pro_namechangeflag_check=='true' or who_pays.replace(' ','')=='MarketCenter' or who_pays=='Region'):
                coaching_prog_data=coaching_prog_data + '<FL val=\"Product Name\">' + str(pro_name).replace('&','%26') + '</FL\
                                          >'+'<FL val=\"Product Before Hold\">' + str(pro_name).replace('&','%26').replace(u"\u2013", " ") + '</FL\
                                          >'+'<FL val=\"Product ID\">' + str(pro_number) + '</FL\
                                          >'+'<FL val=\"Before Hold Product ID\">' + str(pro_number) + '</FL\
                                          >'+'<FL val=\"Current Coach_ID\">' + str(2034239000000171647) + '</FL\
                                          >'+'<FL val=\"SMOWNERID\">' + str(2034239000000115033) + '</FL\
                                           >'+ '<FL val=\"Service Line\">' + str(pro_Service_Line) + '</FL\
                                         >'+ '<FL val=\"Mastery Category\">' + str(pro_Mastery_Category) + '</FL\
                                            >' + '<FL val=\"Price\">' + str(pro_Price) + '</FL\
                                            >' + '<FL val=\"Product Before Hold\">' + str(pro_name).replace('&','%26').replace(u"\u2013", " ") + '</FL\
                                          >' + '<FL val=\"Hold Date Checked\">false</FL\
                                           >' + '<FL val=\"Pay Rate for Product\">' + str(pro_Pay_Rate) + '</FL\
                                           >' + '<FL val=\"Product Name_ID\">' + str(pro_zohoid) + '</FL></row>' + '</CustomModule9>'
                
                
            else:
                coaching_prog_data=coaching_prog_data + '<FL val=\"Product Name\">' + str(pro_name).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Signup Email\">' + str(Signup_Email).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Signup Phone\">' + str(Signup_Phone) + '</FL\
				 >' + '<FL val=\"KWUID\">' + str(kwuid_value)+ '</FL\
                                          >'+'<FL val=\"Coaching Program Name\">' + str(full_name).replace('&','%26')+' '+str(pro_Service_Line).replace('&','%26')+' ' +str(signup_date)+ '</FL\
                                          >'+'<FL val=\"Product Before Hold\">' + str(pro_name).replace('&','%26').replace(u"\u2013", " ") + '</FL\
                                          >'+'<FL val=\"Product ID\">' + str(pro_number) + '</FL\
                                          >'+'<FL val=\"Before Hold Product ID\">' + str(pro_number) + '</FL\
                                          >'+'<FL val=\"Current Coach_ID\">' + str(2034239000000171647) + '</FL\
                                          >'+'<FL val=\"SMOWNERID\">' + str(2034239000000115033) + '</FL\
                                           >'+ '<FL val=\"Service Line\">' + str(pro_Service_Line) + '</FL\
                                         >'+ '<FL val=\"Mastery Category\">' + str(pro_Mastery_Category) + '</FL\
                                            >' + '<FL val=\"Price\">' + str(pro_Price) + '</FL\
                                            >' + '<FL val=\"Product Before Hold\">' + str(pro_name).replace('&','%26').replace(u"\u2013", " ") + '</FL\
                                          >' + '<FL val=\"Hold Date Checked\">false</FL\
                                           >' + '<FL val=\"Pay Rate for Product\">' + str(pro_Pay_Rate) + '</FL\
                                           >' + '<FL val=\"Product Name_ID\">' + str(pro_zohoid) + '</FL></row>' + '</CustomModule9>'
                
        else:
            print('***********else***', previous_coach_id, str(2034239000000171647))

            if (coach_pro_namechangeflag_check=='true' or who_pays.replace(' ','')=='MarketCenter' or who_pays=='Region'):
                coaching_prog_data=coaching_prog_data + '<FL val=\"Product Name\">' + str(pro_name).replace('&','%26') + '</FL\
                                              >'+'<FL val=\"Product Before Hold\">' + str(pro_name).replace('&','%26').replace(u"\u2013", " ")+ '</FL\
                                               >'+'<FL val=\"Product ID\">' + str(pro_number) + '</FL\
                                               >'+'<FL val=\"Before Hold Product ID\">' + str(pro_number) + '</FL\
                                               >'+ '<FL val=\"Service Line\">' + str(pro_Service_Line) + '</FL\
                                               >'+ '<FL val=\"Mastery Category\">' + str(pro_Mastery_Category) + '</FL\
                                                >' + '<FL val=\"Price\">' + str(pro_Price) + '</FL\
                                                >' + '<FL val=\"Product Before Hold\">' + str(pro_name).replace('&','%26').replace(u"\u2013", " ") + '</FL\
                                                >' + '<FL val=\"Hold Date Checked\">false</FL\
                                               >' + '<FL val=\"Pay Rate for Product\">' + str(pro_Pay_Rate) + '</FL\
                                               >' + '<FL val=\"Cancelled Date\">' + str(cancle_date) + '</FL\
                                               >' + '<FL val=\"Product Name_ID\">' + str(pro_zohoid) + '</FL></row>' + '</CustomModule9>'
            else:
                coaching_prog_data=coaching_prog_data + '<FL val=\"Product Name\">' + str(pro_name).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Signup Email\">' + str(Signup_Email).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Signup Phone\">' + str(Signup_Phone) + '</FL\
				 >' + '<FL val=\"KWUID\">' + str(kwuid_value)+ '</FL\
                                              >'+'<FL val=\"Coaching Program Name\">' + str(full_name).replace('&','%26')+' '+str(pro_Service_Line).replace('&','%26')+' ' +str(signup_date)+ '</FL\
                                              >'+'<FL val=\"Product Before Hold\">' + str(pro_name).replace('&','%26').replace(u"\u2013", " ")+ '</FL\
                                               >'+'<FL val=\"Product ID\">' + str(pro_number) + '</FL\
                                               >'+'<FL val=\"Before Hold Product ID\">' + str(pro_number) + '</FL\
                                               >'+ '<FL val=\"Service Line\">' + str(pro_Service_Line) + '</FL\
                                               >'+ '<FL val=\"Mastery Category\">' + str(pro_Mastery_Category) + '</FL\
                                                >' + '<FL val=\"Price\">' + str(pro_Price) + '</FL\
                                                >' + '<FL val=\"Product Before Hold\">' + str(pro_name).replace('&','%26').replace(u"\u2013", " ") + '</FL\
                                                >' + '<FL val=\"Hold Date Checked\">false</FL\
                                               >' + '<FL val=\"Pay Rate for Product\">' + str(pro_Pay_Rate) + '</FL\
                                               >' + '<FL val=\"Cancelled Date\">' + str(cancle_date) + '</FL\
                                               >' + '<FL val=\"Product Name_ID\">' + str(pro_zohoid) + '</FL></row>' + '</CustomModule9>'
                
    elif 'hold'  in product_lower and ac_status=='Active':
        
        print('*************hold************',product_lower,'*************************')
        
        print('\n ****update '+module+' by ' +coaching_prog_id+'with '+str(field_value)+'***\n')
        if ((pro_Mastery_Category.lower()=='group' and existed_cp_product_id!=pro_number) ):
             if (coach_pro_namechangeflag_check=='true' or who_pays.replace(' ','')=='MarketCenter' or who_pays=='Region'):
                coaching_prog_data=coaching_prog_data + '<FL val=\"Product Name\">' + str(pro_name).replace('&','%26').replace(u"\u2013", " ") + '</FL\
                                            >'+'<FL val=\"Product ID\">' + str(pro_number) + '</FL\
                                      >' + '<FL val=\"Account Status\">' + str('Hold') + '</FL\
                                    >' + '<FL val=\"Price\">' + str(pro_Price) + '</FL\
                                     >'+'<FL val=\"Current Coach_ID\">' + str(2034239000000171647) + '</FL\
                                          >'+'<FL val=\"SMOWNERID\">' + str(2034239000000115033) + '</FL\
                                     >' + '<FL val=\"Hold Date\">' + str(hold_date) + '</FL\
                                     >' + '<FL val=\"Product Name_ID\">' + str(pro_zohoid) + '</FL></row>' + '</CustomModule9>'
             else:
                coaching_prog_data=coaching_prog_data + '<FL val=\"Product Name\">' + str(pro_name).replace('&','%26').replace(u"\u2013", " ") + '</FL\
                                     >' + '<FL val=\"Signup Email\">' + str(Signup_Email).replace('&','%26') + '</FL\
                                     >' + '<FL val=\"Signup Phone\">' + str(Signup_Phone) + '</FL\
                                     >' + '<FL val=\"KWUID\">' + str(kwuid_value)+ '</FL\
                                            >'+'<FL val=\"Product ID\">' + str(pro_number) + '</FL\
                                      >' + '<FL val=\"Account Status\">' + str('Hold') + '</FL\
                                    >' + '<FL val=\"Price\">' + str(pro_Price) + '</FL\
                                     >'+'<FL val=\"Current Coach_ID\">' + str(2034239000000171647) + '</FL\
                                          >'+'<FL val=\"SMOWNERID\">' + str(2034239000000115033) + '</FL\
                                     >' + '<FL val=\"Hold Date\">' + str(hold_date) + '</FL\
                                     >' + '<FL val=\"Product Name_ID\">' + str(pro_zohoid) + '</FL></row>' + '</CustomModule9>'
        else:
            if Hold_Date_Checked=='false':
                if (coach_pro_namechangeflag_check=='true' or who_pays.replace(' ','')=='MarketCenter' or who_pays=='Region'):
                    coaching_prog_data=coaching_prog_data + '<FL val=\"Product Name\">' + str(pro_name).replace('&','%26') + '</FL\
                                      >'+'<FL val=\"Product ID\">' + str(pro_number) + '</FL\
                                      >' + '<FL val=\"Account Status\">' + str('Hold') + '</FL\
                                   >' + '<FL val=\"Price\">' + str(pro_Price) + '</FL\
                                   >' + '<FL val=\"Hold Date\">' + str(hold_date) + '</FL\
                                   >' + '<FL val=\"Hold Date Checked\">true</FL\
				 >' + '<FL val=\"Product Name_ID\">' + str(pro_zohoid) + '</FL></row>' + '</CustomModule9>'
                else:
                    coaching_prog_data=coaching_prog_data + '<FL val=\"Product Name\">' + str(pro_name).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Signup Email\">' + str(Signup_Email).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Signup Phone\">' + str(Signup_Phone) + '</FL\
				 >' + '<FL val=\"KWUID\">' + str(kwuid_value)+ '</FL\
                                      >'+'<FL val=\"Product ID\">' + str(pro_number) + '</FL\
                                      >' + '<FL val=\"Account Status\">' + str('Hold') + '</FL\
                                   >' + '<FL val=\"Price\">' + str(pro_Price) + '</FL\
                                   >' + '<FL val=\"Hold Date\">' + str(hold_date) + '</FL\
                                   >' + '<FL val=\"Hold Date Checked\">true</FL\
				 >' + '<FL val=\"Product Name_ID\">' + str(pro_zohoid) + '</FL></row>' + '</CustomModule9>'
            else:
                if (coach_pro_namechangeflag_check=='true' or who_pays.replace(' ','')=='MarketCenter' or who_pays=='Region'):
                    coaching_prog_data=coaching_prog_data + '<FL val=\"Product Name\">' + str(pro_name).replace('&','%26') + '</FL\
                                                     >'+'<FL val=\"Product ID\">' + str(pro_number) + '</FL\
                                                     >' + '<FL val=\"Account Status\">' + str('Hold') + '</FL\
                                                    >' + '<FL val=\"Price\">' + str(pro_Price) + '</FL\
                                                >' + '<FL val=\"Product Name_ID\">' + str(pro_zohoid) + '</FL></row>' + '</CustomModule9>'
                else:
                    coaching_prog_data=coaching_prog_data + '<FL val=\"Product Name\">' + str(pro_name).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Signup Email\">' + str(Signup_Email).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Signup Phone\">' + str(Signup_Phone) + '</FL\
				 >' + '<FL val=\"KWUID\">' + str(kwuid_value)+ '</FL\
                                                     >'+'<FL val=\"Product ID\">' + str(pro_number) + '</FL\
                                                     >' + '<FL val=\"Account Status\">' + str('Hold') + '</FL\
                                                    >' + '<FL val=\"Price\">' + str(pro_Price) + '</FL\
                                                >' + '<FL val=\"Product Name_ID\">' + str(pro_zohoid) + '</FL></row>' + '</CustomModule9>'
   
   
    else:
        coaching_prog_data=coaching_prog_data +'<FL val=\"Product Name_ID\">' + str(pro_zohoid) + '</FL></row>' + '</CustomModule9>'

    coaching_prog_data=coaching_prog_data.replace('&','AND')

    coaching_prog_data=coaching_prog_data.replace('                         ',' ')

    params = {"authtoken":authtoken,"newFormat":1,"xmlData":coaching_prog_data,"scope" : "crmapi","id":coaching_prog_id}
    coaching_prog_up_url="https://crmsandbox.zoho.com/crm/private/json/{}/updateRecords?".format(module)
    print(coaching_prog_id,coaching_prog_data)
    try:
        
        coaching_prog_res=requests.post(coaching_prog_up_url,params=params)
        response=coaching_prog_res.json()
        print(response)
        print (response['response']['result']['message'])
        file=open(os.path.join(mydir_name,filename),'a+')
        file.write(coaching_prog_id+'\t\t\t'+response['response']['result']['recorddetail']['FL'][2]['content']+'\t\t\t'+response['response']['result']['message']+'\t\t\t\n')
        file.close()
        
    except Exception as e:
        email_send('---update into ZOHO of coaching_prog_id '+str(coaching_prog_id)+'-----production_coaching_pro')
        print('coaching_prog****',e)
        file=open(os.path.join(mydir_name,filename),'a+')
        file.write('\t\t\t'+response['response']['error']['message']+'\t\t\t\n')
        file.close()
        
    else:
        try:
            zohoid_cur= conn.cursor()
            processed_day=str((datetime.datetime.now()-datetime.timedelta(0)).strftime('%Y-%m-%d'))

            print( "Update "+ table_name+" set coach_prog_zoho_id="+coaching_prog_id+", updated="+str(True)+", processed_day="+processed_day+" where Subscription_Id="+field_value)
            insert_query = "Update "+ table_name+" set  coach_prog_zoho_id="+coaching_prog_id+", updated="+str(True)+", processed_to_zoho='"+processed_day+"' where Subscription_Id="+field_value
            zohoid_cur.execute(insert_query)
            conn.commit()
            zohoid_cur.close()
        except Exception as e:
            email_send('---update into aws of coaching_prog_id '+str(coaching_prog_id)+'-----production_coaching_pro')
            print('coaching_prog****',e)
            
        
        
#__________________________________________________________________________________________________________

#********-------------- COntact search ----------**********************************************************
#__________________________________________________________________________________________________________
            
def search(expected_value,module,field_label,sub_id):
    global mydir_name
    global filename
    global ratetime
    
    global table_name
    global pro_zohoid
    global coaching_prog_data,subid,pro_number,hold_date,cancle_date,con_data,update_contact_data,coaching_prog_data,chargify_email,chargify_phone
    global pro_name,subid,signup_date,pro_Service_Line,pro_Mastery_Category,pro_Price,pro_rec_price,full_name,pro_Pay_Rate,previous_coach_id,con_zohoid
    
    
    print('entered to search ',expected_value,field_label,'sub id',sub_id)
    authtoken='5f7af2d8ffc3345c6b0228c1e3ed135c'
    #xmlData=con_data
    print('\n ****in search '+module+' by ' +field_label+'='+str(expected_value)+'****\n')
    
    
    url2="https://crmsandbox.zoho.com/crm/private/json/{}/searchRecords?authtoken=5f7af2d8ffc3345c6b0228c1e3ed135c&scope=crmapi&criteria=({}:{})&fromIndex=1&toIndex=200".format(module,field_label,expected_value)
    print('url2--',url2)
    
    try:
        ac=requests.get(url2)
        #print(ac)
        data=ac.json()
        ratetime=ratetime+1
        print(data['response'])

        coaching_prog_data=coaching_prog_data+ '<FL val=\"Contact Changed in CP\">true</FL\
                                 >' + '<FL val=\"Contact Changed Date\">' +str((datetime.datetime.now()-datetime.timedelta(0)).strftime('%Y-%m-%d'))+ '</FL>'
        
        if 'nodata' in data['response']:
            print(data['response']['nodata'],str(chargify_email),str(chargify_phone))
            pushintozoho('Contacts',con_data,expected_value)
            coaching_prog_data=coaching_prog_data+ '<FL val=\"Email\">' + str(chargify_email) + '</FL\
                                 >' + '<FL val=\"Primary Phone\">' + str(chargify_phone) + '</FL>'
            
        if 'result' in data['response']:
            #print(data['response']['result'])
            print('\n ****************************'+ expected_value+'partailly matched *************************** ')
            if data['response']['result']['Contacts']['row']:
            
                dataType= type(data['response']['result']['Contacts']['row'])
                
                # *****records alreday exited**************
                if type(data['response']['result']['Contacts']['row']) is dict:
                    #print(dataType,'--->means single record')
                    print('single records exist   ')
                    #print(data['response']['result']['Contacts']['row']['FL'][0]['content'])
                    #print(type(data['response']['result']['Contacts']['row']['FL']))
                    maps={}
                    for rec_list in data['response']['result']['Contacts']['row']['FL']:
                        maps[rec_list['val']]=rec_list['content']

                    print('maps',maps)
                    if field_label=='KWUID':
                        if field_label in maps.keys():
                            actual_value=maps['KWUID']
                            if actual_value==expected_value:
                                print(field_label,' matched',actual_value,expected_value)
                                con_zohoid=maps['CONTACTID']
                                
                                if 'Email' in maps.keys():
                                    con_Email=maps['Email']
                                else:
                                    con_Email=''                                    
                                if 'Signup Email' in maps.keys():
                                    con_Signup_Email=maps['Signup Email']
                                else:
                                    con_Signup_Email=''
                                if 'Primary Phone' in maps.keys():
                                    con_Primary_Phone=maps['Primary Phone']
                                else:
                                    con_Primary_Phone=''
                                if 'KWUID' in maps.keys():
                                    con_KWUID=maps['KWUID']
                                else:
                                    con_KWUID=''
                                if 'Mailing Street' in maps.keys():
                                    con_Mailing_Street=maps['Mailing Street']
                                else:
                                    con_Mailing_Street=''
                                if 'Mailing City' in maps.keys():
                                    con_Mailing_City=maps['Mailing City']
                                else:
                                    con_Mailing_City=''
                                if 'Mailing State' in maps.keys():
                                    con_Mailing_State=maps['Mailing State']
                                else:
                                    con_Mailing_State=''
                                if 'Mailing Zip' in maps.keys():
                                    con_Mailing_Zip=maps['Mailing Zip']
                                else:
                                    con_Mailing_Zip=''
                                if 'Mailing Country' in maps.keys():
                                    con_Mailing_Country=maps['Mailing Country']
                                else:
                                    con_Mailing_Country=''

                                contact_update_zoho('Contacts',update_contact_data,con_zohoid,expected_value)
                                    

                                coaching_prog_data=coaching_prog_data+'<FL val=\"Email\">' + str(con_Email).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Email\">' + str(con_Email).replace('&','%26') + '</FL\
                                >' + '<FL val=\"Primary Phone\">' + str(con_Primary_Phone) + '</FL\
                                >' + '<FL val=\"Mailing Street\">' + str(con_Mailing_Street) + '</FL\
                               >' + '<FL val=\"Mailing City\">' + str(con_Mailing_City) + '</FL\
                                >' + '<FL val=\"Mailing State\">' + str(con_Mailing_State) + '</FL\
                                >' + '<FL val=\"Mailing Zip\">' + str(con_Mailing_Zip) + '</FL\
                                >' + '<FL val=\"Mailing Country\">' + str(con_Mailing_Country) + '</FL>'
                                    
                                
                                
                                print(con_zohoid,field_label,actual_value)
                                #product_search(pro_id,'Products','Mastery Product ID')
                                #pp_search(sub_id,'Deals','Subscription Id')
                            else:
                                print('kwuid not matched going to insert ',actual_value,expected_value)
                                pushintozoho('Contacts',con_data,expected_value)

                    elif field_label=='Email':
                        if field_label in maps.keys():
                            actual_value=maps['Email']
                            if actual_value==expected_value:
                                print(field_label,' matched',actual_value,expected_value)
                                con_zohoid=maps['CONTACTID']
                                if 'Email' in maps.keys():
                                    con_Email=maps['Email']
                                else:
                                    con_Email=''                                    
                                if 'Signup Email' in maps.keys():
                                    con_Signup_Email=maps['Signup Email']
                                else:
                                    con_Signup_Email=''
                                if 'Primary Phone' in maps.keys():
                                    con_Primary_Phone=maps['Primary Phone']
                                else:
                                    con_Primary_Phone=''
                                if 'KWUID' in maps.keys():
                                    con_KWUID=maps['KWUID']
                                else:
                                    con_KWUID=''
                                    
                                if 'Mailing Street' in maps.keys():
                                    con_Mailing_Street=maps['Mailing Street']
                                else:
                                    con_Mailing_Street=''
                                if 'Mailing City' in maps.keys():
                                    con_Mailing_City=maps['Mailing City']
                                else:
                                    con_Mailing_City=''
                                if 'Mailing State' in maps.keys():
                                    con_Mailing_State=maps['Mailing State']
                                else:
                                    con_Mailing_State=''
                                if 'Mailing Zip' in maps.keys():
                                    con_Mailing_Zip=maps['Mailing Zip']
                                else:
                                    con_Mailing_Zip=''
                                if 'Mailing Country' in maps.keys():
                                    con_Mailing_Country=maps['Mailing Country']
                                else:
                                    con_Mailing_Country=''
                                    
                                contact_update_zoho('Contacts',update_contact_data,con_zohoid,expected_value)
                                    

                                coaching_prog_data=coaching_prog_data+'<FL val=\"Email\">' + str(con_Email).replace('&','%26') + '</FL\
				 >' + '<FL val=\"Email\">' + str(con_Email).replace('&','%26') + '</FL\
                                >' + '<FL val=\"Primary Phone\">' + str(con_Primary_Phone) + '</FL\
                                >' + '<FL val=\"Mailing Street\">' + str(con_Mailing_Street) + '</FL\
                               >' + '<FL val=\"Mailing City\">' + str(con_Mailing_City) + '</FL\
                                >' + '<FL val=\"Mailing State\">' + str(con_Mailing_State) + '</FL\
                                >' + '<FL val=\"Mailing Zip\">' + str(con_Mailing_Zip) + '</FL\
                                >' + '<FL val=\"Mailing Country\">' + str(con_Mailing_Country) + '</FL>'
                                print(con_zohoid,field_label,actual_value)
                                #product_search(pro_id,'Products','Mastery Product ID')
                                #opp_search(sub_id,'Deals','Subscription Id')
                            else:
                                print('email not matched',actual_value,expected_value)
                                pushintozoho('Contacts',con_data,expected_value)
            
                elif dataType is list:
                    matched_recs=len(data['response']['result']['Contacts']['row'])
                    print(dataType, '---means more than one record  ',matched_recs)
                    
                    i=0
                    for rec in data['response']['result']['Contacts']['row']:
                        maps={} 
                        for  field_list  in rec['FL']:
                            maps[field_list['val']]=field_list['content']

                        #print('maps   ',maps)
                        print('field_label',expected_value)
                        if field_label=='KWUID':
                            if field_label in maps.keys():
                                actual_value=maps['KWUID']
                                if actual_value==expected_value:
                                    print(field_label,' matched',actual_value,expected_value)
                                    con_zohoid=maps['CONTACTID']
                                    if 'Email' in maps.keys():
                                        con_Email=maps['Email']
                                    else:
                                        con_Email=''
                                    if 'Signup Email' in maps.keys():
                                        con_Signup_Email=maps['Signup Email']
                                    else:
                                        con_Signup_Email=''
                                    if 'Primary Phone' in maps.keys():
                                        con_Primary_Phone=maps['Primary Phone']
                                    else:
                                        con_Primary_Phone=''
                                    if 'KWUID' in maps.keys():
                                        con_KWUID=maps['KWUID']
                                    else:
                                        con_KWUID=''
                                    if 'Mailing Street' in maps.keys():
                                        con_Mailing_Street=maps['Mailing Street']
                                    else:
                                        con_Mailing_Street=''
                                    if 'Mailing City' in maps.keys():
                                        con_Mailing_City=maps['Mailing City']
                                    else:
                                        con_Mailing_City=''
                                    if 'Mailing State' in maps.keys():
                                        con_Mailing_State=maps['Mailing State']
                                    else:
                                        con_Mailing_State=''
                                    if 'Mailing Zip' in maps.keys():
                                        con_Mailing_Zip=maps['Mailing Zip']
                                    else:
                                        con_Mailing_Zip=''
                                    if 'Mailing Country' in maps.keys():
                                        con_Mailing_Country=maps['Mailing Country']
                                    else:
                                        con_Mailing_Country=''

                                    print(con_zohoid,field_label,actual_value)

                                    contact_update_zoho('Contacts',update_contact_data,con_zohoid,expected_value)

                                    coaching_prog_data=coaching_prog_data+'<FL val=\"Email\">' + str(con_Email).replace('&','%26') + '</FL\
				                 >' + '<FL val=\"Email\">' + str(con_Email).replace('&','%26') + '</FL\
                                                 >' + '<FL val=\"Primary Phone\">' + str(con_Primary_Phone) + '</FL\
                                                 >' + '<FL val=\"Mailing Street\">' + str(con_Mailing_Street) + '</FL\
                                                 >' + '<FL val=\"Mailing City\">' + str(con_Mailing_City) + '</FL\
                                                 >' + '<FL val=\"Mailing State\">' + str(con_Mailing_State) + '</FL\
                                                 >' + '<FL val=\"Mailing Zip\">' + str(con_Mailing_Zip) + '</FL\
                                                 >' + '<FL val=\"Mailing Country\">' + str(con_Mailing_Country) + '</FL>'
                                    
                                    #product_search(pro_id,'Products','Mastery Product ID')
                                    #opp_search(sub_id,'Deals','Subscription Id')
                                    break
                                else:
                                    print('kwuid not matched',actual_value,expected_value)
                                    i=i+1
                                    
                                    if i==matched_recs:
                                        print(i)
                                        print('going to insert')
                                        pushintozoho('Contacts',con_data,expected_value)

                        elif field_label=='Email':
                            if field_label in maps.keys():
                                actual_value=maps['Email']
                                if actual_value==expected_value:
                                    print(field_label,' matched',actual_value,expected_value)
                                    con_zohoid=maps['CONTACTID']
                                    if 'Email' in maps.keys():
                                        con_Email=maps['Email']
                                    else:
                                        con_Email=''
                                    if 'Signup Email' in maps.keys():
                                        con_Signup_Email=maps['Signup Email']
                                    else:
                                        con_Signup_Email=''
                                    if 'Primary Phone' in maps.keys():
                                        con_Primary_Phone=maps['Primary Phone']
                                    else:
                                        con_Primary_Phone=''
                                    if 'KWUID' in maps.keys():
                                        con_KWUID=maps['KWUID']
                                    else:
                                        con_KWUID=''
                                    if 'Mailing Street' in maps.keys():
                                        con_Mailing_Street=maps['Mailing Street']
                                    else:
                                        con_Mailing_Street=''
                                    if 'Mailing City' in maps.keys():
                                        con_Mailing_City=maps['Mailing City']
                                    else:
                                        con_Mailing_City=''
                                    if 'Mailing State' in maps.keys():
                                        con_Mailing_State=maps['Mailing State']
                                    else:
                                        con_Mailing_State=''
                                    if 'Mailing Zip' in maps.keys():
                                        con_Mailing_Zip=maps['Mailing Zip']
                                    else:
                                        con_Mailing_Zip=''
                                    if 'Mailing Country' in maps.keys():
                                        con_Mailing_Country=maps['Mailing Country']
                                    else:
                                        con_Mailing_Country=''

                                    print(con_zohoid,field_label,actual_value)

                                    contact_update_zoho('Contacts',update_contact_data,con_zohoid,expected_value)

                                    coaching_prog_data=coaching_prog_data+'<FL val=\"Email\">' + str(con_Email).replace('&','%26') + '</FL\
				                 >' + '<FL val=\"Email\">' + str(con_Email).replace('&','%26') + '</FL\
                                                 >' + '<FL val=\"Primary Phone\">' + str(con_Primary_Phone) + '</FL\
                                                 >' + '<FL val=\"Mailing Street\">' + str(con_Mailing_Street) + '</FL\
                                                 >' + '<FL val=\"Mailing City\">' + str(con_Mailing_City) + '</FL\
                                                 >' + '<FL val=\"Mailing State\">' + str(con_Mailing_State) + '</FL\
                                                 >' + '<FL val=\"Mailing Zip\">' + str(con_Mailing_Zip) + '</FL\
                                                 >' + '<FL val=\"Mailing Country\">' + str(con_Mailing_Country) + '</FL>'
                                    
                                    #product_search(pro_id,'Products','Mastery Product ID')
                                    #opp_search(sub_id,'Deals','Subscription Id')
                                    break
                                else:
                                    print('email not matched',actual_value,expected_value)
                                    i=i+1
                                    print(i)
                                    if i==matched_recs:
                                        print('going to insert')
                                        pushintozoho('Contacts',con_data,expected_value)



    except Exception as e:
        print(e)
            

def pushintozoho(module,con_xmlData,field_name):
    global mydir_name
    global filename
    global ratetime
    
    global table_name
    global pro_zohoid
    global coaching_prog_data,subid,pro_number,hold_date,cancle_date
    global pro_name,subid,signup_date,pro_Service_Line,pro_Mastery_Category,pro_Price,pro_rec_price,full_name,pro_Pay_Rate,previous_coach_id,con_zohoid
    #print('filename ', filename)
    print('\n ****** INSERT **********\n',con_xmlData)
    authtoken='5f7af2d8ffc3345c6b0228c1e3ed135c'
    xmlData=con_xmlData
    field_name=field_name
    print('field_name ,',field_name)
    print('module ,',module,'  con_zohoid ',con_zohoid)
    #con_zohoid=''
    #pprint(xmlData)
    params = {"authtoken":authtoken,"newFormat":1,"xmlData":con_xmlData,"scope" : "crmapi"}
    url="https://crmsandbox.zoho.com/crm/private/json/{}/insertRecords?".format(module)
    print(url)
    #authtoken=5f7af2d8ffc3345c6b0228c1e3ed135c&scope=crmapi&newFormat=1&xmlData="+xmlData
    
    #print ('dssdsd',data)
    try:
        ac=requests.post(url,params=params)
        print(ac)
        data=ac.json()
        ratetime=ratetime+1
        print(data['response'])
        
        if (data['response']['result']['recorddetail']['FL']):
            #print(i)
            print('\n\n -- ',data['response']['result']['message'])
            print('\n\n record id --',data['response']['result']['recorddetail']['FL'][0]['content'],'\n')
            con_zohoid=data['response']['result']['recorddetail']['FL'][0]['content']
            print('---zoho id----after inserted ---',con_zohoid)
            
            file=open(os.path.join(mydir_name,filename),'a+')

            file.write(con_zohoid+'\t\t\t'+data['response']['result']['recorddetail']['FL'][2]['content']+'\t\t\t'+data['response']['result']['message']+'\t\t\t\n')
            file.close()
        else:
            email_send('product_cocahing_pro.py failed while inserting contact due to'+str(data['response']))
            print('product_cocahing_pro.py failed while inserting contact due to'+str(data['response']))
            
    except Exception as e:
        email_send('product_cocahing_pro.py failed while inserting contact due to'+str(e))
        print('pushintozoho **** Error *** : ',data['response']['error']['message'])
        return 'pushintozoho **** Error *** : ',data['response']['error']['message']
        file=open(os.path.join(mydir_name,filename),'a+')

        file.write('\t\t\t'+data['response']['result']['message']+'\t\t\t\n')
        file.close()


#________________________________________________________________________________________________________________
#                       *******COntact Updation method **********
#________________________________________________________________________________________________________________

def contact_update_zoho(module,xmlData,zohoid,field_value):
    global filename
    global table_name
    global ratetime
    global db_field_lable
    
    #print('filename ', filename)
    
    print('\n********update method************\n')
    authtoken='5f7af2d8ffc3345c6b0228c1e3ed135c'
    xmlData=xmlData
    print('\n \n in update----',xmlData)
    #userid=userid
    
    #print(userid)
    #print('---------------',xmlData)
    params = {"authtoken":authtoken,"newFormat":1,"xmlData":xmlData,"scope" : "crmapi","id":zohoid}
    url="https://crmsandbox.zoho.com/crm/private/json/{}/updateRecords?".format(module)
    print(url)
    #authtoken=5f7af2d8ffc3345c6b0228c1e3ed135c&newFormat=1&scope=crmapi&id="+zohoid+"&xmlData="+xmlData
    #authtoken=5f7af2d8ffc3345c6b0228c1e3ed135c&scope=crmapi&newFormat=1&xmlData="+xmlData
    
     #print ('dssdsd',data)
    try:
        ac=requests.post(url,params=params)
        #print(ac)
        data=ac.json()
        ratetime=ratetime+1
        #print('data')
        #print('====update try----',data['response']['result']['recorddetail']['FL'][2]['content'])
        print (data['response']['result']['message'])
        #status=str(data['response']['result']['message'])
        file=open(os.path.join(mydir_name,filename),'a+')

        file.write(data['response']['result']['message']+'\t')
        file.close()
        '''try:
            print('---zoho id----after inserted ---',zohoid, "Update "+ table_name+ " set  zoho_id="+zohoid+",integrated_to_zoho="+str(True)+" where "+db_field_lable+"="+field_value)
            check_true_cur= conn.cursor()
            #update_query="INSERT INTO Staging_Users_Table(first_name) VALUES ('fgsdkjfhdjkfhjk')"
            #print(zoho_id)
            
            update_query = "Update "+ table_name+ " set  zoho_id="+zohoid+",integrated_to_zoho="+str(True)+" where "+db_field_lable+"="+field_value
            print(update_query)
            check_true_cur.execute(update_query)
            conn.commit()
            check_true_cur.close()
        except Exception as e:
            print(e)
            email_send('')'''
        
    
    
    except Exception as e:        
        print('update **** Error *** : ',data['response']['error']['message'])
        email_send(' chargify to zoho Contact Updation Failed for this KWUID or Email '+str(field_value))
        file=open(os.path.join(mydir_name,filename),'a+')

        file.write(zohoid+'\t\t\t'+data['response']['error']['message']+'\t\t\t\n')
        file.close()      

    else:
        print('updatezoho ok')



sub_handler()

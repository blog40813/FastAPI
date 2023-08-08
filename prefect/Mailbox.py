import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from tool import GlobalVars
#from tool.application import Application,WebApplication
import configparser


#config = configparser.ConfigParser()
#config.read(GlobalVars.DEFAULT_CONFIG_PATH)
#usr = config.get('COMMANDLINE','sso_id')
#pwd = config.get('COMMANDLINE','sso_passwd')

def mail2_admin(content,list,cclist=[]):
    sender="itri461776@itri.org.tw"
    content="<p>"+content+"</p>"
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = ';'.join(list)
    msg["Cc"] = ';'.join(cclist)
    msg["Subject"] = "[異常通知]vm13監測系統"
    _msg = MIMEText(content)
    _msg["Content-Type"] = "text/html"
    msg.attach(_msg)
    print("success")
    try:
        smtp = smtplib.SMTP("smtpx.itri.org.tw")
        smtp.ehlo(name="itri.org.tw")
        smtp.login(user="461776", password="Blog40813@itri")
        addr=list
        smtp.sendmail(from_addr=sender, to_addrs=addr+cclist, msg=msg.as_string())
    except Exception as e:
        print("Mail: "+str(e))
    finally:
        smtp.quit()
        
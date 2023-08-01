from prefect import flow
from prefect.context import get_run_context
from prefect_email import EmailServerCredentials, email_send_message
from typing import List
from Mailbox import mail2_admin
'''
from prefect.orion.schemas.schedules import CronSchedule
from prefect.orion.schemas import schedules

from prefect.server.schemas.schedules import CronSchedule
from prefect.server.schemas import schedules

'''

'''
credentials = EmailServerCredentials(
    username="bscffybbb@gmail.com",
    password="ofvialrhaksbrhlh",  # must be an app password
    host="smtp.gmail.com",  
    port=587,  # 連接埠，Gmail 使用的是 587

)
credentials.save("test",overwrite= True)
'''

'''
credentials = EmailServerCredentials(
    username="love900687@gmail.com",
    password="earzcvmatuyqdshx",  # must be an app password
    host="smtp.gmail.com",  
    port=587,  # 連接埠，Gmail 使用的是 587

)
credentials.save("test2",overwrite= True)
'''


'''

credentials = EmailServerCredentials(
    username="blog40813@outlook.com",
    password="jkusmhwbikkphopi",  # must be an app password
    host="smtp-mail.outlook.com",  
    port=587,  # 連接埠，Gmail 使用的是 587
    smtp_type="STARTTLS"

)

credentials.save("test3",overwrite= True)
'''
#EmailServerCredentials.load("test2")

@flow
def example_email_send_message_flow(email_addresses: List[str]):
    email_server_credentials = EmailServerCredentials.load("test2")
    for email_address in email_addresses:
        subject = email_send_message.with_options(name=f"email {email_address}").submit(
            email_server_credentials=email_server_credentials,
            subject="Example Flow Notification using Gmail",
            msg="This proves email_send_message works!(desktop)",
            email_to=email_addresses
        )
#example_email_send_message_flow(["itri461776@itri.org.tw"])




def notify_exc_by_email(exc):
    context = get_run_context()
    flow_run_name = context.flow_run.name
    email_server_credentials = EmailServerCredentials.load("test3")
    email_send_message(
        email_server_credentials=email_server_credentials,
        subject=f"Flow run {flow_run_name!r} failed",
        msg=f"Flow run {flow_run_name!r} failed due to {exc}.",
        email_to="as27198455@yahoo.com.tw",
    )

list = ["blog40813@gmail.com","love900687@gmail.com"]
cclist = ["itri461776@itri.org.tw","tonyhsieh@itri.org.tw"]

@flow
def example_flow():
    try:
        1 / 0
    except Exception as exc:
        mail2_admin("Server test sent to multiple receiver",list)
        mail2_admin("CCCCCCCCCCCCCCCCC",list,cclist)
        raise

#example_flow()


"""
​@flow 裝飾器來設定 Schedule 是不支援的。@flow 裝飾器用於定義 Prefect 的流程，而 Schedule 的設定通常是透過 Flow 的參數來完成。

@task
def my_task():
    print("Hello, Prefect!")

# 定義 IntervalSchedule，這個例子設定每隔 1 分鐘執行一次
schedule = IntervalSchedule(interval=timedelta(minutes=1))

# 創建 Flow，並將 Schedule 設定為前面定義的 schedule
flow = Flow("My Flow", schedule=schedule)
result = my_task()

# 建立 Flow，並將 Schedule 設定為前面定義的 schedule
with Flow("My Flow", schedule=schedule) as flow:
    result = my_task()

# 執行 Flow
flow.run()


"""

if __name__  == "__main__":
    example_flow()
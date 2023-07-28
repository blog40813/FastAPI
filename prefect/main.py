from prefect import flow
from prefect.context import get_run_context
from prefect_email import EmailServerCredentials, email_send_message
from typing import List

'''
credentials = EmailServerCredentials(
    username="bscffybbb@gmail.com",
    password="ofvialrhaksbrhlh",  # must be an app password
    host="smtp.gmail.com",  
    port=587,  # 連接埠，Gmail 使用的是 587

)
credentials.save("test",overwrite= True)
'''
credentials = EmailServerCredentials(
    username="love900687@gmail.com",
    password="earzcvmatuyqdshx",  # must be an app password
    host="smtp.gmail.com",  
    port=587,  # 連接埠，Gmail 使用的是 587
    smtp_type="SSL"

)
credentials.save("test2",overwrite= True)

EmailServerCredentials.load("test2")

@flow
def example_email_send_message_flow(email_addresses: List[str]):
    email_server_credentials = EmailServerCredentials.load("test2")
    for email_address in email_addresses:
        subject = email_send_message.with_options(name=f"email {email_address}").submit(
            email_server_credentials=email_server_credentials,
            subject="Example Flow Notification using Gmail",
            msg="This proves email_send_message works!",
            email_to=email_address,
        )

example_email_send_message_flow(["test"])




def notify_exc_by_email(exc):
    context = get_run_context()
    flow_run_name = context.flow_run.name
    email_server_credentials = EmailServerCredentials.load("email-server-credentials")
    email_send_message(
        email_server_credentials=email_server_credentials,
        subject=f"Flow run {flow_run_name!r} failed",
        msg=f"Flow run {flow_run_name!r} failed due to {exc}.",
        email_to="blog40813@gmail.com",
    )
'''
@flow
def example_flow():
    try:
        1 / 0
    except Exception as exc:
        notify_exc_by_email(exc)
        raise

example_flow()
'''
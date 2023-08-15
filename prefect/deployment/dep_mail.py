import os 
import sys
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(),os.pardir))


from mail import Mail

from prefect.deployments import Deployment
from prefect.filesystems import RemoteFileSystem
from prefect.infrastructure import DockerContainer
 
dep_mail = Deployment.build_from_flow(
    name="Sending_email",
    flow=Mail
)
dep_mail.apply()
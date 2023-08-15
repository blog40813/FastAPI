
import os 
import sys
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(),os.pardir))

from transfer import Excel

from prefect.deployments import Deployment
from prefect.filesystems import RemoteFileSystem
from prefect.infrastructure import DockerContainer
 
dep_excel = Deployment.build_from_flow(
    name="Txt_to_excel",
    flow=Excel
)
dep_excel.apply()

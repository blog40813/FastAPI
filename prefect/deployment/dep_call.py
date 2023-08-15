
import os 
import sys
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(),os.pardir))

from call_api import Call_api

from prefect.deployments import Deployment
from prefect.filesystems import RemoteFileSystem
from prefect.infrastructure import DockerContainer
 
dep_call = Deployment.build_from_flow(
    name="Call_164",
    flow=Call_api
)
dep_call.apply()
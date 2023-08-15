
import os 
import sys
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(),os.pardir))

from plot import Plot

from prefect.deployments import Deployment
from prefect.filesystems import RemoteFileSystem
from prefect.infrastructure import DockerContainer
 
dep_plot = Deployment.build_from_flow(
    name="Generate chart",
    flow=Plot
)
dep_plot.apply()
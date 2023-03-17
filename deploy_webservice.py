import os

from azureml.core import Workspace, Environment, Model
from azureml.core.webservice import AciWebservice, Webservice
from azureml.core.model import InferenceConfig


def get_workspace():
    """
    Connect to Azure ML Workspace using config.json file, which is the default value for this function.
    """

    ws = Workspace.from_config()
    return ws


def register_environment(ws):
    """
    Register custom environment into Azure ML Workspace.
    Args:
        ws (azure.core.Workspace): azure ML workspace where ML model is registered
    """

    myenv = Environment(name='odbc_env')
    myenv.from_dockerfile('odbc_env', path_to_Dockerfile)
    myenv.register(ws)


def deploy_webservice(ws, env):
    """
    Deploy webservice to environment given by the service name.
    Args:
        ws (azure.core.Workspace): azure ML workspace where ML model and environment is registered
    """

    source_directory = os.path.join(os.getcwd(), os.environ['ARTIFACT_PATH'], 'src')

    model = Model(ws, os.environ['MODEL_NAME'], version=os.environ['MODEL_VERSION'])
    inference_config = InferenceConfig(
        entry_script='script.py',
        source_directory=source_directory,
        environment=env)

    deployment_config = AciWebservice.deploy_configuration(cpu_cores=1.8,
                                                           memory_gb=7,
                                                           dns_name_label=os.environ['DNS_NAME'],
                                                           enable_app_insights=True)
    service = Model.deploy(ws, os.environ['WEB_SERVICE_NAME'], [model], inference_config, deployment_config, overwrite=True)
    service.wait_for_deployment(True)


def main():
    """
    Run webservice deployment using custom environment from Dockerfile.
    """

    ws = get_workspace()
    env = register_environment(ws)
    deploy_webservice(ws, env)

if __name__ == '__main__':
    main()


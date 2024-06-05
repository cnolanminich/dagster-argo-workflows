from dagster import ConfigurableResource, AssetExecutionContext
import argo_workflows
from argo_workflows.api import workflow_service_api
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow_create_request import (
    IoArgoprojWorkflowV1alpha1WorkflowCreateRequest,)
import time


class ArgoResource(ConfigurableResource):
    def run_workflow(manifest, context: AssetExecutionContext):
        # local host for Argo
        configuration = argo_workflows.Configuration(host="https://127.0.0.1:2746")
        # ONLY for local Argo / local kubernetes
        configuration.verify_ssl = False
        api_client = argo_workflows.ApiClient(configuration)
        api_instance = workflow_service_api.WorkflowServiceApi(api_client)
        workflow = IoArgoprojWorkflowV1alpha1WorkflowCreateRequest(workflow=manifest, _check_type=False)
        created_workflow = api_instance.create_workflow('argo', workflow, _check_return_type=False)
        context.log.info(f"Workflow {created_workflow['metadata']['name']} created")
        # Wait for the workflow to finish
        start_time = time.time() 
        while True:
            current_workflow = api_instance.get_workflow('argo', created_workflow['metadata']['name'], _check_return_type=False)
            if current_workflow['status']['finishedAt']:
                break
            elapsed_time = time.time() - start_time  # calculate the elapsed time
            if elapsed_time > 600:  # 600 seconds = 10 minutes
                raise Exception("Timeout: Workflow did not finish within 10 minutes.")
            
            time.sleep(10)  # wait for 10 seconds before checking the status again
        return current_workflow

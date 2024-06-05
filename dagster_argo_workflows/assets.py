from dagster import AssetExecutionContext, asset, MaterializeResult, DataVersion, MetadataValue
import requests
import yaml
from dagster_argo_workflows.resources import ArgoResource
from datetime import datetime
import pytz 


@asset
def example_argo_asset(context: AssetExecutionContext):
    context.log.info("Started computation")

    resp = requests.get('https://raw.githubusercontent.com/argoproj/argo-workflows/main/examples/hello-world.yaml')
    manifest = yaml.safe_load(resp.text)
    
    current_workflow = ArgoResource.run_workflow(manifest, context)
    
    context.log.info(current_workflow)
    context.log.info(f"Workflow {current_workflow['metadata']['name']} started at {current_workflow['status']['startedAt']} and finished at {current_workflow['status']['finishedAt']}")
    finished_at_str = current_workflow['status']['finishedAt']
    finished_at_datetime = datetime.strptime(finished_at_str, "%Y-%m-%dT%H:%M:%SZ") 
    finished_at_datetime = finished_at_datetime.replace(tzinfo=pytz.UTC)
    return MaterializeResult(
        metadata={
            "finished_at": MetadataValue.timestamp(finished_at_datetime),
            "workflow_name": MetadataValue.text(current_workflow['metadata']['name'])
        }
    )

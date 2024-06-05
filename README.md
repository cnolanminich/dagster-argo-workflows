# dagster-argo-workflows
 
Example of how to execute Argo workflows from Dagster via the `argo-workflows` python pacakge.


## What You'll Need to run this locally

- [kind](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [kubectl](https://kubernetes.io/docs/reference/kubectl/)




## Packages you'll need

On MacOS:
`brew install kind kubectl docker`
`brew install --cask docker`
`brew install argo`  if you want to test argo using the Argo CLI


## Setting up kind cluster + getting started with Argo locally

`kind create cluster`
`export ARGO_WORKFLOWS_VERSION="v3.5.7"`
`kubectl config use-context kind-kind`
`kubectl port-forward svc/argo-server 2746:2746 -n argo`

## Running the Dagster project

`pip install -e ".[dev]"`

Get started
`dagster dev`




from setuptools import find_packages, setup

setup(
    name="dagster_argo_workflows",
    packages=find_packages(exclude=["dagster_argo_workflows"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "requests",
        "argo-workflows",
        "pyyaml",
        "pytz"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)

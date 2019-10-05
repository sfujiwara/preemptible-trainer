import os
import googleapiclient.discovery
import requests


def get_instance_group_name() -> str:
    """
    Description
    -----------
    Get managed instance group name from metadata.

    Returns
    -------
    instance_group_name:
        Managed instance group name.
    """

    res = requests.get(
        url='http://metadata/computeMetadata/v1/instance/attributes/created-by',
        headers={'Metadata-Flavor': 'Google'}
    )
    instance_group_name = os.path.basename(str(res.content, 'utf-8'))

    return instance_group_name


def resize_instance_group(instance_group: str, project: str, zone: str, size: int) -> None:

    compute = googleapiclient.discovery.build('compute', 'v1')
    res = compute.instanceGroupManagers().resize(
        project=project,
        zone=zone,
        instanceGroupManager=instance_group,
        size=size,
    ).execute()

    return res


def get_instance_name() -> str:
    """
    Description
    -----------
    Get Google Compute Engine instance name from meta data server.

    Returns
    -------
    instance_name:
        Instance name.
    """

    res = requests.get(
        url='http://metadata/computeMetadata/v1/instance/name',
        headers={'Metadata-Flavor': 'Google'}
    )
    instance_name = str(res.content, 'utf-8')

    return instance_name


def get_project_id() -> str:
    """
    Description
    -----------
    Get GCP project ID from meta data server.

    Returns
    -------
    project_id:
        Project ID.
    """

    res = requests.get(
        url='http://metadata/computeMetadata/v1/project/project-id',
        headers={'Metadata-Flavor': 'Google'}
    )
    project_id = str(res.content, 'utf-8')

    return project_id


def get_zone() -> str:
    """
    Description
    -----------
    Get zone of Compute Engine instance from meta data server.

    Returns
    -------
    zone:
        Zone of Compute Engine instance.
    """

    res = requests.get(
        url='http://metadata/computeMetadata/v1/instance/zone',
        headers={'Metadata-Flavor': 'Google'}
    )
    zone = str(res.content, 'utf-8')
    zone = zone.split('/')[-1]

    return zone


def delete_instance(project, zone, instance):

    compute = googleapiclient.discovery.build('compute', 'v1')

    res = compute.instances().delete(
        project=project,
        zone=zone,
        instance=instance
    ).execute()

    return res


def self_delete():

    project_id = get_project_id()
    zone = get_zone()
    instance_name = get_instance_name()

    delete_instance(project=project_id, zone=zone, instance=instance_name)


def self_resize_instance_group(size: int) -> None:

    project_id = get_project_id()
    zone = get_zone()
    instance_group_name = get_instance_group_name()

    resize_instance_group(
        project=project_id,
        zone=zone,
        instance_group=instance_group_name,
        size=size,
    )

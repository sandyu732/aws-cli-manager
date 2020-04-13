import boto3
import botocore
import click

session = boto3.Session(profile_name='sandy')
ec2_session = session.resource('ec2')

def get_instances(project):
    instances = []
    if project:
        filters = [{'Name': 'tag:Project', 'Values': ["{0}".format(project)]}]
        instances = ec2_session.instances.filter(Filters=filters)
    else:
        instances = ec2_session.instances.all()
    return instances

def has_pending_snapshot(volume):
    snapshot = list(volume.snapshots.all())
    return snapshot and snapshot[0].state == "pending"

@click.group()
def cli():
    """Command Line Manager"""

@cli.group('instances')
#@click.option('--profile', required=True, type=str, help='Provide the AWS profile name')
def instances():
    """Commands for Instances"""

@cli.group('volumes')
def volumes():
    """Commands for EBS Volumes"""

@cli.group('snapshots')
def snapshots():
    """Commands for Snapshots"""

@snapshots.command('list')
@click.option('--project', default=None, show_default=True, help="Display all the available snapshots of instances in project")
@click.option('--all', 'list_all', default=False, is_flag=True, help='List all the snapshots for the given volume, and not just recent ones.')
def list_snapshots(project, list_all):
    """List the available snapshots for the instances"""
    instances = get_instances(project)
    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(', '.join((
                    s.snapshot_id,
                    s.volume_id,
                    i.id,
                    s.state,
                    s.description)))
                
                if s.state == "completed" and not list_all: break
    return

@volumes.command('list')
@click.option('--project', default=None, show_default=True, help="Display Volumes attached to the instances in project")
def list_volumes(project):
    """List the EBS Volumens along with their associated EC2 instances"""
    instances = get_instances(project)
    for i in instances:
        tags = { t['Key'] : t['Value'] for t in i.tags or [] }
        for v in i.volumes.all():
            print(', '.join((
            v.id,
            i.id,
            v.state,
            v.availability_zone,
            str(v.size) + "GiB",
            str(v.create_time),
            v.encrypted and "Encrypted" or "Non encrypted",
            tags.get('Project', 'Unknown Project'))))
    return


@instances.command('list', help='Command to list the EC2 istances.')
@click.option('--project', default=None, show_default=True, help="Filter's instances for provided project name")
def list_instances(project):
    instances = get_instances(project)

    for i in instances:
        tags = { t['Key'] : t['Value'] for t in i.tags or [] }
        print(', '.join((
            i.id,
            i.instance_type,
            i.state['Name'],
            i.placement['AvailabilityZone'],
            i.image_id,
            i.public_dns_name,
            str(i.public_ip_address),
            tags.get('Project', 'No Project Name'))
            )
        )
    return

@instances.command('stop', help='Command to stop the ec2 instances')
@click.option('--project', default=None, help="Filter's instances for provided project name")
def stop_instances(project):
    instances = get_instances(project)

    for i in instances:
        print("Stopping the {0},,,,,".format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print("Could not stop {0} instance".format(i.id) + str(e))
            continue
    return

@instances.command('start', help='Command to start the ec2 instances')
@click.option('--project', default=None, help="Filter's instances only for provided project name")
def start_instances(project):
    instances = get_instances(project)

    for i in instances:
        print("Starting the {0} instance".format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print("Could not start {0} instance".format(i.id) + str(e))
            continue
    return

@instances.command('snapshots', help='Command to create snapshot of the ec2 instances')
@click.option('--project', default=None, help="Filter's instances only for provided project name")
def create_snapshots(project):
    instances = get_instances(project)

    for i in instances:
        print("Stopping {0} instance.".format(i.id))
        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all():
            if has_pending_snapshot(v):
                print("Skipping {0} snapshot already in progress".format(v.id))
                continue
            print("Creating snapshot for {0} ebs volume.".format(v.id))
            v.create_snapshot(Description='Snapshot created by Sandy CLI Tool')
        
        print("Starting {0} instance".format(i.id))
        i.start()
        i.wait_until_running()

    print("Snapshot creation completed!")
    return
        
if __name__ == "__main__":
    cli()
    

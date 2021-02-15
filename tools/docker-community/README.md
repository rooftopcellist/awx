# Installing Community AWX

## Configuration

Configure your AWX installation by setting variables in the `inventory` file (`tools/ansible/inventory`).  At a minimum, the `admin_password` needs to be set.  

## Installation

After setting any needed variables in the  `inventory` file, run the following make command from the top level of your awx clone to start AWX containers.  

> Note: If you are coming from a Local Docker installation of AWX, consider migrating your data first using `tools/ansible/migrate.yml`.  See the data migration section below.  

```
make awx-release
```


## Migrating Data from Local Docker

If you are migrating data from a Local Docker installation (17.0.1 and prior), you can 
migrate your data to the Community AWX Docker Compose installation by doing the following.  

1. Set the following variables.....
2. Run the migrate playbook to migrate your data to the new postgresql container and convert the data directory to a volume mount.  

If you had a custom pgdocker or awxcompose location, you will need to set these variables:

```
postgres_data_dir: "~/.awx/pgdocker"
old_docker_compose_dir: "~/.awx/awxcompose"
```

```
ansible-playbook -i inventory migrate.yml -e "migrate_local_docker=true" --ask-become
```


## Building your own image

Typically, you will want to use the official images provided on quay.io.  If you want to build your own AWX image locally, you can do the following:

```
ansible-playbook -i inventory build.yml -e awx_version=test-build
```

> Note that this would build an image tagged devel.  

To run this container, in `vars.yml`, set the value of `awx_docker_actual_image` to that of your newly built container image.  

```
awx_docker_actual_image=ansible/awx:devel
```

Then run the containers
```
make run-awx
```

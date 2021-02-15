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
migrate your data to the Community AWX Docker Compose installation via the migrate.yml playbook, or by using the manual steps described below.  

### Migrate data with migrate.yml

1. Set the following variables.....
2. Run the migrate playbook to migrate your data to the new postgresql container and convert the data directory to a volume mount.  

If you had a custom pgdocker or awxcompose location, you will need to set these variables:

```
postgres_data_dir: "~/.awx/pgdocker"
old_docker_compose_dir: "~/.awx/awxcompose"
```

```
ansible-playbook -i inventory migrate.yml -e "migrate_local_docker=true" -e "postgres_data_dir=~/.awx/pgdocker" -e "old_docker_compose_dir=~/.awx/awxcompose" --ask-become
```

> Note: This requires you to provide your become passwords to be able to access the postgresql data directory.  

3. Change directory to `tools/ansible` and start your containers

```
cd tools/ansible
ansible-playbook -i inventory install.yml -vv
```

4. After ensuring your data has been successfully migrated, you may delete your old data directory (typically stored at `~/.awx/pgdocker`). 


### Migrating data manually

1. With Local Docker still running, perform a pg_dumpall:

> Note: If Local Docker is no longer running
`docker-compose -f ~/.awx/awxcompose/docker-compose.yml up postgres`

docker-compose -f ~/.awx/awxcompose/docker-compose.yml exec postgres pg_dumpall -U awx > awx_dump.sql


2. Remove all local docker containers (specifically awx_postgres)

```
docker -f rm awx_postgres
```

3. Template the new docker-community compose

```
ansible-playbook -i tools/ansible/inventory tools/ansible/sources.yml
```

4. Start a container with a volume (using the new tools/docker-community/docker-compose-community.yml)

```
docker-compose -f ../docker-community/docker-compose-community.yml up postgres
```

5. Restore to new `awx_postgres`
```
docker-compose -f ../docker-community/docker-compose-community.yml exec -T postgres psql -U awx -d awx -p 5432 < awx_dump.sql
```

6. Run the docker-community compose to start the containers

```
docker-compose -f ../docker-community/docker-compose-community.yml up task
```

7. Check to ensure your data migration was successful, then you can delete your the `awx_dump.sql` backup and your old data directory.  


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
cd tools/ansible
ansible-playbook -i inventory install.yml -vv
```

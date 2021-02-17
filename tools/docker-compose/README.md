# Docker Compose for Dev container

## Overview

Here are the main make targets and files:

* `docker-compose-build` - used for building the development image, which is used by both `docker-compose` and `docker-compose-community`.  
* `docker-compose` - Make target for development, passes awx_devel image and tag.  
* `docker-compose-community` - uses awx_devel image published to quay.io.  
* `tools/docker-compose/inventory` file - used to configure the local AWX development deployment.  
* `migrate.yml` - playbook for migrating data from Local Docker to the Development Environment.  

## Configuration

In the  `inventory` file, set your `pg_password`, `broadcast_websocket_secret`, `secret_key`, and any other settings you need for your deployment.  

An external database can be used by setting the `pg_host`, `pg_hostname`, and `pg_username`.  

> Note: If you are coming from a Local Docker installation of AWX, consider migrating your data first, see the [data migration section](#migrating-data-from-local-docker) below.  


## Starting the Development Environment

Below is the recommended way to install AWX locally for use, for more developer specific notes, see the [Setting up your development environment](./../../CONTRIBUTING.md#setting-up-your-development-environment) doc.  

### Building a custom image (optional)
In the root directory of your awx clone, run the following to build your docker image.  
This step takes a while, but once your image is built, you don't need to do this again 
unless you make changes to the Dockerfile or any of the files used by the Dockerfile.  

```bash
$ make docker-compose-build
```

> Note: By default, this image will be tagged with your branch name.  You can specify a custom tag by setting an environment variable, for example: `DEVEL_IMAGE_NAME=quay.io/ansible/awx_devel:17.0.1`

### Run AWX

Run the awx, postgres and redis containers
```bash
$ make docker-compose-community
```
> Note: You may need to add `COMPOSE_TAG=<yourbranch>` at the end of this to use the correct image for your branch.  

Clean and Build UI
```bash
$ docker exec tools_awx_1 make clean-ui ui-devel
```

The app should now be accessible in your browser at `https://localhost:8043/#/home`

## Migrating Data from Local Docker

If you are migrating data from a Local Docker installation (17.0.1 and prior), you can 
migrate your data to the development environment via the migrate.yml playbook, or by using the manual steps described below.  

> Note: This will also convert your postgresql bind-mount into a docker volume.

### Migrate data with migrate.yml

If you had a custom pgdocker or awxcompose location, you will need to set the `postgres_data_dir` and `old_docker_compose_dir` variables. 

1. Run the [migrate playbook](./ansible/migrate.yml) to migrate your data to the new postgresql container and convert the data directory to a volume mount.
```bash
$ ansible-playbook migrate.yml -e "migrate_local_docker=true" -e "postgres_data_dir=~/.awx/pgdocker" -e "old_docker_compose_dir=~/.awx/awxcompose"
```


2. Change directory to the top of your awx checkout and start your containers
```bash
$ make docker-compose-community
```

3. After ensuring your data has been successfully migrated, you may delete your old data directory (typically stored at `~/.awx/pgdocker`). 


### Migrating data manually

1. With Local Docker still running, perform a pg_dumpall:
> Note: If Local Docker is no longer running
`docker-compose -f ~/.awx/awxcompose/docker-compose.yml up postgres`

  ```bash
  $ docker-compose -f ~/.awx/awxcompose/docker-compose.yml exec postgres pg_dumpall -U awx > awx_dump.sql
  ```

2. Remove all local docker containers (specifically awx_postgres)
```bash
$ docker -f rm awx_postgres
```

3. Template the new docker-community compose
```bash
$ ansible-playbook -i tools/ansible/inventory tools/ansible/sources.yml
```

4. Start a container with a volume (using the new tools/docker-community/docker-compose-community.yml)
```bash
$ docker-compose -f ../docker-community/docker-compose-community.yml up postgres
```

5. Restore to new `awx_postgres`
```bash
$ docker-compose -f ../docker-community/docker-compose-community.yml exec -T postgres psql -U awx -d awx -p 5432 < awx_dump.sql
```

6. Run the docker-community compose to start the containers
```bash
$ docker-compose -f ../docker-community/docker-compose-community.yml up task
```

7. Check to ensure your data migration was successful, then you can delete your the `awx_dump.sql` backup and your old data directory.  


## Extras
* [Using Logstash](./docs/logstash.md)

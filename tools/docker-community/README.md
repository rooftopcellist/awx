# Installing Community AWX

## Configuration

Configure your AWX installation by setting variables in the `vars.yml` file in this directory.  At a minimum, the `admin_password` needs to be set.  

## Installation

After setting any needed variables in `vars.yml`, run the following make command from the top level of your awx clone to start AWX containers.  

```
make awx-release
```


## Migrating Data from Local Docker

If you are migrating data from a Local Docker installation (17.0.1 and prior), you can 
migrate your data to the Community AWX Docker Compose installation by doing the following.  

1. Set the following variables.....
2. Run the migrate playbook to migrate your data to the new postgresql container and convert the data directory to a volume mount.  

```
ansible-playbook local -e @vars.yml migrate.yml
```


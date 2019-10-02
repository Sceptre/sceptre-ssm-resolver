# Overview

The purpose of this resolver is to retrieve values from the AWS SSM. 

## Install

```bash
pip install sceptre-ssm-resolver
```

## Available Resolvers

### ssm

Fetches the value stored in AWS SSM Parameter Store.

Syntax:

```yaml
parameter|sceptre_user_data:
    <name>: !ssm /prefix/param
```

#### Example:

Add a secure string to the SSM parameter store
```bash
aws ssm put-parameter --name /dev/DbPassword --value "mysecret" \
--key-id alias/dev/kmskey --type "SecureString"
```

Setup sceptre template to retrieve and decrypt from parameter store
```yaml
parameters:
    database_password: !ssm /dev/DbPassword
```

Run sceptre with a user or role that has access to the secret.
Sceptre will retrieve "mysecret" from the parameter store and passes
it to the cloudformation _database_password_ paramter.

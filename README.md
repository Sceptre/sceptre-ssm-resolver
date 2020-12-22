# Overview

The purpose of this resolver is to retrieve values from the AWS SSM. 

## Install

```bash
pip install sceptre-ssm-resolver
```

## Available Resolvers

### ssm

Fetches the value stored in AWS SSM Parameter Store.

__Note:__ Sceptre must be run with a user or role that has access to the parameter store

Syntax:

```yaml
parameter|sceptre_user_data:
  <name>: !ssm /prefix/param
```

```yaml
parameter|sceptre_user_data:
  <name>: !ssm
    name: /prefix/param
    profile: OtherAccount
```

```yaml
parameter|sceptre_user_data:
  <name>: !ssm {"name": "/prefix/param", "profile": "OtherAccount"}
```


#### Example:

Add a secure string to the SSM parameter store
```bash
aws ssm put-parameter --name /dev/DbPassword --value "mysecret" \
--key-id alias/dev/kmskey --type "SecureString"
```

Retrieve and decrypt SSM parameter from the same account that the
stack is being deployed to:
```yaml
parameters:
  database_password: !ssm /dev/DbPassword
```

Retrieve and decrypt SSM parameter from another AWS account:
```yaml
parameters:
  database_password: !ssm
    name: /dev/DbPassword
    profile: OtherAccount
```

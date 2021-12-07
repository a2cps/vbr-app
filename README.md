# VBR Api

## Deployment

The current version of the API is deployed at http://vbr-api.a2cps.canyonero.info
Interactive docs can be found at http://vbr-api.a2cps.canyonero.info/docs and more 
detailed API docs can be found at http://vbr-api.a2cps.canyonero.info/redoc

Deployment is managed automatically by the AWS App Runner service in response 
to pushes of `a2cps/vbr_api` to an A2CPS-internal Amazon Elastic Container Registry. 

This process is automated via the `deploy` Makefile target.


import pulumi
import logging

from cognito import CognitoSetup
from generic.init.initConfigurator import InitConfigurator


########################
# Intialize basic configuration of project #
########################

init_config = InitConfigurator()
flag = init_config.initialize()

########################
# IaC setup #
########################

# Create Cognito pool and setup Configuration
cognitoSetup = CognitoSetup()

# Create User Pool
userPool = cognitoSetup.create_user_pool()

# Create SAML Identity Provider for Okta
identityProvider = cognitoSetup.create_identity_provider(userPool.id)

# Create App Client for User Pool
userPoolAppClient = cognitoSetup.create_user_pool_appclient(userPool.id, identityProvider)

# Create Domain for App Client
userPoolDomain = cognitoSetup.create_user_pool_domain(userPool.id)



# Details of Cognito Infrastructure Setup on AWS"

pulumi.export('User Pool Id     => ', userPool.id)
pulumi.export('User Pool Name   => ', userPool.name)
pulumi.export('App Client Id    => ', userPoolAppClient.id)
pulumi.export('App Client Name  => ', userPoolAppClient.name)
# pulumi.export('Identity Provider Resource Name  => ', identityProvider.resource_name)
pulumi.export('Identity Provider Id  => ', identityProvider.id)



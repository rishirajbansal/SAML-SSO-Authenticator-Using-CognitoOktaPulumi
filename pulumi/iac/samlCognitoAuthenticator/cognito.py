import os

import pulumi
import pulumi_aws as aws


class CognitoSetup:

    def create_user_pool(self):
        userPool = aws.cognito.UserPool(os.getenv("AWS_COGNITO_USER_POOL_RES_NAME"),
                                        auto_verified_attributes=None,
                                        name=os.getenv("AWS_COGNITO_USER_POOL_NAME"),
                                        username_attributes=None,
                                        # Commenting required attributes as it is handled by Okta
                                        # and also on enabling it, prevents Cognito to update the user if request comes
                                        # from Okta SAML
                                        # schemas=[
                                        #     {
                                        #         'name': 'email',
                                        #         'required': True,
                                        #         'attributeDataType': 'String'
                                        #     }
                                        # ],
                                        password_policy={
                                            'minimumLength': 8,
                                            'requireLowercase': False,
                                            'requireNumbers': False,
                                            'requireSymbols': False,
                                            'requireUppercase': False
                                        }
                                        )

        return userPool

    def create_user_pool_appclient(self, userPool_id, identityProvider):
        userPoolAppClient = aws.cognito.UserPoolClient(os.getenv("AWS_COGNITO_USER_POOL_APP_CLIENT_RES_NAME"),
                                                       name=os.getenv("AWS_COGNITO_USER_POOL_APP_CLIENT_NAME"),
                                                       generate_secret=True,
                                                       allowed_oauth_flows_user_pool_client=True,
                                                       explicit_auth_flows=[
                                                           'ALLOW_ADMIN_USER_PASSWORD_AUTH',
                                                           'ALLOW_USER_PASSWORD_AUTH',
                                                           'ALLOW_USER_SRP_AUTH',
                                                           'ALLOW_REFRESH_TOKEN_AUTH'
                                                       ],
                                                       allowed_oauth_flows=[
                                                           'code',
                                                           'implicit'
                                                       ],
                                                       allowed_oauth_scopes=['phone', 'email', 'openid', 'profile', 'aws.cognito.signin.user.admin'],
                                                       callback_urls=[os.getenv("AWS_COGNITO_CALLBACK_URL")],
                                                       logout_urls=[os.getenv("AWS_COGNITO_CALLBACK_URL")],
                                                       default_redirect_uri=os.getenv("AWS_COGNITO_CALLBACK_URL"),
                                                       supported_identity_providers=['COGNITO', os.getenv("AWS_COGNITO_IDENTITY_PROVIDER_NAME")],
                                                       user_pool_id=userPool_id,
                                                       opts=pulumi.ResourceOptions(
                                                           depends_on=[
                                                               identityProvider
                                                           ]
                                                           # depends_on=[
                                                           #     pulumi.Resource(
                                                           #         t='aws.cognito.IdentityProvider',
                                                           #         name=os.getenv("AWS_COGNITO_IDENTITY_PROVIDER_RES_NAME"),
                                                           #         custom=False
                                                           #     )
                                                           # ]
                                                       )
                                                       )

        return userPoolAppClient

    def create_user_pool_domain(self, userPool_id):
        userPoolDomain = aws.cognito.UserPoolDomain(os.getenv("AWS_COGNITO_USER_POOL_DOMAIN_RES_NAME"),
                                                    domain=os.getenv("AWS_COGNITO_USER_POOL_DOMAIN_NAME"),
                                                    user_pool_id=userPool_id
                                                    )

        return userPoolDomain

    def create_identity_provider(self, userPool_id):
        identityProvider = aws.cognito.IdentityProvider(os.getenv("AWS_COGNITO_IDENTITY_PROVIDER_RES_NAME"),
                                                        provider_name=os.getenv("AWS_COGNITO_IDENTITY_PROVIDER_NAME"),
                                                        provider_type='SAML',
                                                        provider_details={
                                                            'MetadataURL': os.getenv("AWS_COGNITO_SAML_PROVIDER_OKTA_METADATA_URL")
                                                        },
                                                        attribute_mapping={
                                                            'email': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress'
                                                        },
                                                        user_pool_id=userPool_id
                                                        )

        return identityProvider


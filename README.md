# SAML-SSO-Authenticator-Using-CognitoOktaPulumi

The objective of the project is to allow Nuage’s staff users to securely login into the Django Admin application from one-click login without using a password. This will make easier for users to access the application faster and avoiding the hassle to providing the login credentials everytime. This will also provide a feature if the user does not exist in the Django Admin system but coming from secure authenticated system to access Django admin, its record will be created on run time in Django, hence enhancing ease of operational activities of User Management.

This application sorts out an issue of common problem, if user needs to access multiple applications where each app requires a different set of credentials, it becomes a hassle for the end user. First, the user will need to remember different passwords - in addition to any other corporate password that may already exist. The user is now forced to maintain separate usernames and passwords, dealing with different password policies and expirations.

It emerges the need for SSO (Single Sign On) implementation.

The main challenge was how to add secure authentication system to let allow users without providing login credentials. SAML authentication base system was chosen to implement this problem. 

The SAML authentication flow is asynchronous. The Service Provider does not know if the Identity Provider will ever complete the entire flow. Because of this, the Service Provider does not maintain any state of any authentication requests generated. When the Service Provider receives a response from an Identity Provider, the response must contain all the necessary information.

A SAML IdP will generate a SAML response based on configuration that is mutually agreed upon by the IdP and the SP. Upon receiving the SAML assertion, the SP needs to validate that the assertion comes from a valid IdP and then parse the necessary information from the assertion: the username, attributes, etc. 

The approach is figured out to use Okta as a SAML IdP provider and AWS Cognito as a liaison for SP Provider for Django Admin. AWS Cognito manages the user’s SAML authentication process by generating a SAML Authentication Request that gets redirected to the IdP which further connects to AWS Cognito with SAML Response and from there it gets redirected further to Django Admin application. Django application further authenticate SAML request based on the tokens and retrieve the user details from AWS Cognito by sharing token details. If token details are found valid by Cognito, it will send user details back to Django admin and user will finally be allowed to access the application. 

AWS Cognito is configured dynamically with SAML based Identity Provider details. In order to fulfill the needs of the IdP configuration for completing the SAML setup, metadata URL based relationship is established between SP and IdP. Metadata is preferred because it can handle any future additions/enhancements in SAML.

Django Admin application supports both SAML based authentication system and email/password authentication system so as to avoid any downtime issues of IdP (Okta) and not to stop users to access the application. Customized User Management system for Django Admin is developed to sync the users with Cognito.

To make the Cognito infrastructure dynamically configurable and one-click creation, IaC templates are build-up to automated the process of Cognito components setup. This will avoid any manual handling of Cognito. To implement this automation Pulumi tool is used which provides range of APIs to manage, setup & configure AWS Cognito dynamically.


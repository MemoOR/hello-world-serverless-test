# Serverless Framework template with layers, mfa, scripts and CI/CD with actions

To use this template add to your repository secrets the next variables:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_MFA_KEY               #you get it from the first time you ativate mfa in your account
AWS_MFA_SERIAL_NUMBER     #you get it from the first time you ativate mfa in your account
AWS_IAM_ROLE              #your lambda execution role arn if you have one
SERVERLESS_ACCESS_KEY     #Get it from your serverless account
```

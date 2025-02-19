# Test readme

## Running the tests

To run all tests you can use the `run_tests.bat` file in the tests folder.
This bat file sets up a new virtual environment and installs the package before running all tests.

Alternatively you can run each test file separately by simply running them as Python scripts.

## SMTP

For testing SMTP you need [Mailpit](https://mailpit.axllent.org/) running on localhost.

Since smtp_util uses STARTTLS you need to configure Mailpit for this. [More info here.](https://mailpit.axllent.org/docs/configuration/smtp/#smtp-with-starttls)

By default the tests use the following cofigurations for Mailpit:

- Host: localhost
- smtp port: 1025
- http port: 8025

These can be changed by using the environment variables:

- mailpit_host
- mailpit_smtp_port
- mailpit_http_port

Use this command to generate the TLS certificates:

```bash
openssl req -x509 -newkey rsa:4096 -nodes -keyout key.pem -out cert.pem -sha256
```

And this command to launch Mailpit:

```bash
mailpit --smtp-tls-cert cert.pem --smtp-tls-key key.pem
```

## Environment variables

You need to setup a .env file in the root directory with the following parameters:

### SAP

SAP_LOGIN = 'login;password'
SAP_NEW_PASSWORD = 'new password'

If SAP_NEW_PASSWORD is not set, the change password test is skipped.

### GRAPH

GRAPH_API = '{"client_id":"something", "tenant_id":"something", "username":"something", "password":"something"}'

MAIL_USER = "test@email.dk"
MAIL_FOLDER1 = "Indbakke/Graph Test/Undermappe"
MAIL_FOLDER2 = "Indbakke/Graph Test/Undermappe2"

### KMD Nova

NOVA_PARTY = '6101009805,Test Test'
NOVA_DEPARTMENT = '{"id": 818485,"name": "Borgerservice","user_key": "4BBORGER"}'
NOVA_CREDENTIALS = 'nova_login,nova_password'
NOVA_USER = '{"name": "svcitkopeno svcitkopeno", "ident": "AZX0080", "uuid": "0bacdddd-5c61-4676-9a61-b01a18cec1d5"}'
NOVA_USER_GROUP = '{"name": "ÅÅÅ_Frontoffice", "ident": "819697", "uuid": "144d7ab7-302f-4c62-83d2-dcdefcd92dea"}'

NOVA_CVR_CASE = '{"cvr": "55133018", "case_title": "rpa_testcase", "case_number": "S2024-25614"}'
NOVA_CPR_CASE = '{"cpr": "6101009805", "case_title": "Meget_Unik_Case_Overskrift", "case_number": "S2023-61078"}'
NOVA_GROUP_CASE = '{"cpr": "6101009805", "case_title": "Testsag brugergruppe", "case_number": "S2025-5318"}'

Note: The NOVA_CVR_CASE and NOVA_CPR_CASE variables require cases to be created in Nova, and the parameters set from those cases.

### CVR API

CVR_CREDS = 'login;password'

### EFLYT

EFLYT_LOGIN = 'username,password'
TEST_CPR = 'XXXXXXXXXX'
TEST_CASE = '123456' # A test case with multiple current inhabitants, with relations registered
TEST_CASE_NOONE = '56789' # A test case without any current inhabitants

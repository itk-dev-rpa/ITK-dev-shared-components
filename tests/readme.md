# Test readme

## Running the tests

To run all tests you can use the `run_tests.bat` file in the tests folder.
This bat file sets up a new virtual environment and installs the package before running all tests.

Alternatively you can run each test file separately by simply running them as Python scripts.

## Environment variables
You need to setup a .env file in the root directory with the following parameters:

GRAPH_API = '{"client_id":"something", "tenant_id":"something", "username":"something", "password":"something"}'
SAP_LOGIN = 'login;password'

MAIL_USER = "test@email.dk"
MAIL_FOLDER1 = "Indbakke/Graph Test/Undermappe"
MAIL_FOLDER2 = "Indbakke/Graph Test/Undermappe2"

NOVA_PARTY = '6101009805,Test Test'
NOVA_DEPARTMENT = '{"id": 818485,"name": "Borgerservice","user_key": "4BBORGER"}'
NOVA_CREDENTIALS = 'nova_login,nova_password'
NOVA_USER = '{"name": "svcitkopeno svcitkopeno", "ident": "AZX0080", "uuid": "0bacdddd-5c61-4676-9a61-b01a18cec1d5"}'

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

## System requirements
### Nova
To be able to run tests, you must have the following cases created in the system, for a CVR and a CPR:

    cvr = "55133018"
    case_title = "rpa_testcase"
    case_number = "S2024-25614"

    cpr = "6101009805"
    case_title = "Meget_Unik_Case_Overskrift"
    case_number = "S2023-61078"
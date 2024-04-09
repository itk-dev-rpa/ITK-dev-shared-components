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
mailpit --smtp-tls-cert /path/to/cert.pem --smtp-tls-key /path/to/key.pem
```
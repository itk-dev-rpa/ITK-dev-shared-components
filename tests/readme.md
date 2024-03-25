# Test readme

## SMTP

For testing SMTP you need [Mailpit](https://mailpit.axllent.org/) running on localhost.

Since smtp_util uses STARTTLS you need to configure Mailpit for this. [More info here.](https://mailpit.axllent.org/docs/configuration/smtp/#smtp-with-starttls)

By default the tests use the following ports for Mailpit:
- smtp: 1025
- http: 8025

These can be changed in `test_smtp/test_smtp_util.py`.
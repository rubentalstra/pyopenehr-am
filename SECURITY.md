# Security policy

This project parses openEHR artefacts (**ADL2 / ODIN / BMM / OPT2**) and treats
all inputs as **untrusted**.

## Reporting a vulnerability

Please **do not** open a public GitHub issue for security-sensitive reports.

- Preferred: use GitHub’s private vulnerability reporting:
  https://github.com/rubentalstra/pyopenehr-am/security/advisories/new

Include as much as you can:

- affected version(s)
- impact (what could an attacker do?)
- minimal reproduction steps
- a minimized sample input (ADL/ODIN/BMM/OPT), if possible

We’ll aim to acknowledge reports within a few business days.

## Non-security bugs

For normal bugs, feature requests, or non-sensitive parser/validation issues,
please open a regular issue: https://github.com/rubentalstra/pyopenehr-am/issues

## Secure-by-design notes

Engineering notes for working with untrusted inputs live in:

- [docs/security.md](docs/security.md)

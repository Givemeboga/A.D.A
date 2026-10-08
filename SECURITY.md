# Security policy

Ada is a personal project that runs on a home network, but security is part of the design and reports are welcome.

## Reporting a vulnerability

Please **do not open a public issue** for a security problem. Use GitHub's private reporting instead:
**Security → Report a vulnerability** on this repository.

Useful to include: what you found, how to reproduce it, and which phase or file it affects.
I will reply within a week.

## In scope

- Ways to make Ada run a tool without the owner's confirmation
- Prompt injection that reaches the planner from web pages, notes or other untrusted content
- Ways to reach Ada's services from outside the LAN or Tailscale
- Secrets or personal data committed to this repository

## Out of scope

- Attacks that need physical access to the owner's machines
- Weaknesses in the upstream models or libraries themselves (please report those upstream)

## If you find a committed secret

Tell me privately. I will rotate it first and then rewrite history; deleting a file is not enough.

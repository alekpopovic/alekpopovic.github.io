# Newsletter publication

The archive is `/newsletter/`; the first issue is `/newsletter/2026-10/`.
`_data/newsletters.yml` drives the archive and `/newsletter.xml` Atom feed. Article and update feeds are live without
an email provider. No visitor email addresses are collected by the Jekyll site.

To enable email signup, the owner must supply an existing provider's public
HTTPS subscription form URL. Set `newsletter_url` in `_config.yml`, rebuild,
and check the link on `/subscribe/` and `/newsletter/`. Test a subscription in
the provider account, including confirmation and unsubscribe. A valid link
alone does not prove email delivery.

Prepare one issue each month when there is substantive new work. Select a few
articles, explain what changed, link the original material, and preview the
message on a phone. Copy the reviewed web issue into the owner's email service
and send from that account. This repository does not send messages or hold
provider credentials. For each new issue, add a default-layout page under `newsletter/` and a stable
ID, date, title, description and URL in `_data/newsletters.yml`. Search, sitemap,
newsletter feed and publication checks include it automatically. Do not add
placeholder issues or claim that a web issue was emailed.

Never claim an active email subscription or a successful campaign until the
owner has configured the service and checked receipt. Keep RSS available.

## Suggested owner setup: Brevo

1. Create an account and a contact list, such as CodePop newsletter.
2. Choose an existing sender mailbox on a domain the owner controls. Add that
   sending domain in Settings → Senders, Domains, IPs → Domains. Copy the exact
   Brevo code, DKIM, and DMARC instructions into the domain's DNS host. Inspect
   an existing DMARC record before changing it, especially for Workspace mail.
3. Open Marketing → Forms → Sign-up and create a public signup form with an
   email field. Enable double opt-in and review the confirmation message.
4. Copy the public HTTPS form link from Share. Set it as `newsletter_url`;
   rebuild and publish. This link-based integration needs no API credential.
5. Subscribe using a test address, confirm the subscription, preview a message,
   check receipt and unsubscribe before announcing email signup.

Provider instructions checked on 2026-10-12:
[signup forms](https://help.brevo.com/hc/en-us/articles/208771869-Create-a-sign-up-form-in-Brevo)
and [domain authentication](https://help.brevo.com/hc/en-us/articles/12163873383186-Authenticate-your-domain-with-Brevo-Brevo-code-DKIM-DMARC).

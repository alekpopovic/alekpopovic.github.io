## Chapter 7 - Human Authentication and Session Security

The reference platform implements provider-neutral authentication in Go and PostgreSQL. This avoids a mandatory managed identity service, but it also means the application owns password handling, token rotation, session revocation, MFA, rate limits, and account recovery.

### Separate identity classes

At minimum, define distinct authentication paths for:

- human users;
- tracking devices;
- API clients;
- public-share links;
- internal process roles.

A human access token must not authenticate a GPS device. A device credential must not open the dashboard. Reusing one token model across identity classes makes scope mistakes likely.

### Password registration

Normalize email addresses according to a documented policy. Do not attempt provider-specific rewriting such as removing dots unless the product explicitly owns that behavior. Store the original display value separately if needed.

Passwords should be hashed with a memory-hard algorithm such as Argon2id. Store algorithm parameters with the hash so they can be upgraded.

```text
$argon2id$v=19$m=65536,t=3,p=2$...salt...$...hash...
```

On successful login, compare in constant time and opportunistically rehash when the configured policy becomes stronger. Put an upper bound on accepted password length before hashing to avoid resource-exhaustion attacks while still allowing password managers.

### Access and refresh tokens

Use short-lived signed access tokens and rotating opaque refresh tokens. Access tokens carry only necessary claims:

```json
{
  "iss": "tracking-platform",
  "sub": "user-id",
  "sid": "session-id",
  "org": "selected-organization-id",
  "aud": "control-api",
  "iat": 1791630000,
  "exp": 1791630900
}
```

Permissions can be loaded from the database rather than embedded in long-lived tokens. This makes revocation and role changes effective quickly.

Refresh tokens are random opaque values. Store only a cryptographic hash:

```text
refresh_tokens
  id
  user_id
  session_id
  family_id
  token_hash
  issued_at
  expires_at
  rotated_at
  revoked_at
  replaced_by_id
```

Every use rotates the token. Reuse of an already rotated token indicates theft or a client race. Revoke the family, record a security event, and require reauthentication.

### Session inventory

Users should see active sessions with approximate device, browser, IP region, creation time, and last use. They can revoke one session or all others. Do not store more network metadata than the security purpose requires.

The server checks session status during refresh and for sensitive step-up operations. For very short access-token lifetimes, per-request database checks may not be necessary, but high-risk endpoints can require a fresh session verification.

### Email verification and password reset

Verification and reset tokens are random, single-use, short-lived, and hashed at rest. Responses should not reveal whether an email address exists.

A safe reset workflow:

1. accept an email address and return a generic response;
2. create a hashed token only for an eligible account;
3. enqueue a delivery job;
4. validate token hash, purpose, expiry, and unused status;
5. set the new password and invalidate the token;
6. revoke existing refresh families according to policy;
7. write an audit and security event.

Links should not include user identifiers that create unnecessary enumeration opportunities.

### MFA and step-up authentication

Time-based one-time passwords are a portable second factor. Encrypt the TOTP secret with an application key stored outside the database. Generate one-time recovery codes and store their hashes.

Enabling MFA is itself a state machine:

```text
not_configured -> pending_verification -> enabled -> disabled
```

Do not mark it enabled until a valid code proves the authenticator was configured.

Step-up authentication can be required for:

- changing credentials;
- viewing recovery codes;
- exporting precise location history;
- creating long-lived API clients;
- changing retention or privacy settings;
- disabling MFA;
- accessing emergency or guardian features.

Record `auth_time` or a server-side step-up grant and require it to be recent.

### Login defenses

Defend against both account targeting and distributed credential stuffing:

- per-account and per-network rate limits;
- exponential delays after repeated failures;
- generic errors;
- suspicious-login events;
- breached-password checks where operationally acceptable;
- device and session history;
- optional temporary challenges;
- no secrets in logs.

Rate limits should have bounded database cost. A dedicated table with expiring counters can work at moderate scale, but benchmark contention. In-process token buckets may supplement, not replace, durable account lock policy.

### Signing-key rotation

Access-token signing keys need identifiers and a rotation procedure. Verifiers accept current and previous public keys during an overlap period. New tokens use the new key. Retire old keys only after all tokens they signed have expired.

Store private key material in mounted secret files with strict permissions. Do not bake it into images or write it to database migrations.

### Chapter checklist

The human authentication system should provide:

- memory-hard password hashing with upgrade capability;
- short access tokens and rotating opaque refresh tokens;
- refresh-family reuse detection;
- user-visible session inventory and revocation;
- single-use hashed verification and reset tokens;
- MFA enrollment, recovery codes, and step-up rules;
- layered rate limits and security events;
- tested signing-key rotation.

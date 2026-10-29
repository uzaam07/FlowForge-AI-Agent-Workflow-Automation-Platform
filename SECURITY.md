# Security policy and controls

Controls included: Argon2 password hashing; expiring JWTs; server-side role checking; owner-scoped database queries; typed/length-limited request schemas; graph validation; rate limiting; explicit CORS allowlist; security headers; request-size guard; no API secrets in frontend; HTTP workflow nodes disabled.

Known limitations: no external penetration test; no email verification/reset/MFA/token revocation; localStorage bearer token; database `create_all` instead of formal migrations; IP rate limiting needs reverse-proxy configuration; no durable worker; demo AI is deterministic and not an LLM. Do not describe this starter as unhackable. Run dependency audits and review deployment settings before public use.

Admin access is not granted during public registration. Provision an admin role only through a trusted database operation or a protected out-of-band admin process.

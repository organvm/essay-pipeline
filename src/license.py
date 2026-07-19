"""Offline HMAC license keys for the essay-pipeline template library.

A license key is a signed, *readable* token that encodes which product
(``sku``) was purchased, by whom (``email``), when (``issued``), and optionally
when access ends (``expires``). The signature is an HMAC-SHA256 over that
payload, truncated and base32-encoded.

Verification is fully offline: the same shared secret that signs a key also
verifies it. This is the classic "HMAC key check" gate — it deters casual
sharing and copying of the premium templates without requiring an activation
server. It is intentionally *not* a DRM system: anyone holding the secret can
mint keys, so the secret is the asset to protect. Production sellers MUST set
``ESSAY_PIPELINE_LICENSE_SECRET`` to a private value and issue keys with it;
the bundled default exists only so the gate is exercisable out of the box.

CLI:
    python -m src.license issue --email buyer@example.com --sku premium-bundle
    python -m src.license issue --email buyer@example.com \
        --sku premium-subscription --expires 2026-07-19
    python -m src.license verify --key EPK1.<payload>.<sig>
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import os
import sys
from dataclasses import dataclass
from datetime import date

KEY_PREFIX = "EPK1"
SIG_BYTES = 16  # 128-bit truncated HMAC tag; ample for an offline gate
FIELD_SEP = "|"
SEGMENT_SEP = "."

# Demo-only signing secret. Real sellers override via ESSAY_PIPELINE_LICENSE_SECRET.
DEFAULT_SECRET = b"organvm-essay-pipeline-demo-secret-v1"

# SKUs the store knows how to sell. Maps a SKU to the template tiers it unlocks.
KNOWN_SKUS = {
    "premium-bundle": "Every premium template in the catalog",
    "premium-single": "A single premium template (see purchase receipt)",
    "premium-subscription": "Premium access for an active subscription period",
}

SUBSCRIPTION_SKUS = {"premium-subscription"}


class LicenseError(Exception):
    """Raised when a license key is malformed, tampered with, or unsigned."""


@dataclass(frozen=True)
class License:
    """A verified license payload."""

    sku: str
    email: str
    issued: str
    expires: str | None = None

    def covers_premium(self, as_of: date | str | None = None) -> bool:
        """Whether this license grants access to premium templates."""
        if self.sku not in KNOWN_SKUS:
            return False
        if self.sku in SUBSCRIPTION_SKUS and not self.expires:
            return False
        if not self.expires:
            return True

        try:
            expires_on = date.fromisoformat(self.expires)
            check_date = _coerce_date(as_of)
        except ValueError:
            return False
        return check_date <= expires_on


def _coerce_date(value: date | str | None = None) -> date:
    if value is None:
        return date.today()
    if isinstance(value, date):
        return value
    return date.fromisoformat(value)


def _get_secret(secret: bytes | str | None = None) -> bytes:
    """Resolve the signing/verification secret.

    Precedence: explicit argument > ESSAY_PIPELINE_LICENSE_SECRET env var >
    bundled demo default.
    """
    if secret is not None:
        return secret if isinstance(secret, bytes) else secret.encode("utf-8")
    env_secret = os.environ.get("ESSAY_PIPELINE_LICENSE_SECRET")
    if env_secret:
        return env_secret.encode("utf-8")
    return DEFAULT_SECRET


def _b32(raw: bytes) -> str:
    """Unpadded uppercase base32 (license-key friendly)."""
    return base64.b32encode(raw).decode("ascii").rstrip("=")


def _unb32(text: str) -> bytes:
    """Inverse of :func:`_b32`, restoring base32 padding."""
    pad = (-len(text)) % 8
    return base64.b32decode(text.upper() + ("=" * pad))


def _sign(payload: str, secret: bytes) -> bytes:
    return hmac.new(secret, payload.encode("utf-8"), hashlib.sha256).digest()[:SIG_BYTES]


def issue_license(
    email: str,
    sku: str = "premium-bundle",
    issued: str | None = None,
    expires: str | None = None,
    secret: bytes | str | None = None,
) -> str:
    """Mint a signed license key.

    Args:
        email: Buyer identity embedded in the key.
        sku: Product purchased (see :data:`KNOWN_SKUS`).
        issued: ISO date string; defaults to today.
        expires: Optional ISO date after which access is no longer granted.
        secret: Override signing secret (else env var / demo default).

    Returns:
        A license key string of the form ``EPK1.<payload>.<sig>``.

    Raises:
        LicenseError: If email or sku contain the field separator.
    """
    issued = issued or date.today().isoformat()
    if any(FIELD_SEP in value for value in (email, sku, expires or "")):
        raise LicenseError(f"email, sku, and expires must not contain {FIELD_SEP!r}")

    fields = [sku, email, issued]
    if expires:
        fields.append(expires)
    payload = FIELD_SEP.join(fields)
    sig = _sign(payload, _get_secret(secret))
    return SEGMENT_SEP.join(
        [KEY_PREFIX, _b32(payload.encode("utf-8")), _b32(sig)]
    )


def verify_license(key: str, secret: bytes | str | None = None) -> License:
    """Verify a license key and return its payload.

    Raises:
        LicenseError: If the key is malformed or the signature does not match.
    """
    if not isinstance(key, str):
        raise LicenseError("license key must be a string")

    parts = key.strip().split(SEGMENT_SEP)
    if len(parts) != 3 or parts[0] != KEY_PREFIX:
        raise LicenseError("unrecognized license key format")

    _, payload_b32, sig_b32 = parts
    try:
        payload = _unb32(payload_b32).decode("utf-8")
        provided_sig = _unb32(sig_b32)
    except (ValueError, UnicodeDecodeError) as exc:
        raise LicenseError(f"corrupt license key: {exc}") from exc

    expected_sig = _sign(payload, _get_secret(secret))
    if not hmac.compare_digest(provided_sig, expected_sig):
        raise LicenseError("license signature mismatch (wrong secret or tampered key)")

    fields = payload.split(FIELD_SEP)
    if len(fields) not in {3, 4}:
        raise LicenseError("license payload has unexpected shape")

    sku, email, issued = fields[:3]
    expires = fields[3] if len(fields) == 4 else None
    return License(sku=sku, email=email, issued=issued, expires=expires)


def is_valid(key: str | None, secret: bytes | str | None = None) -> bool:
    """Convenience boolean check; never raises."""
    if not key:
        return False
    try:
        verify_license(key, secret)
        return True
    except LicenseError:
        return False


def _cmd_issue(args: argparse.Namespace) -> int:
    if args.sku not in KNOWN_SKUS:
        print(f"WARNING: '{args.sku}' is not a known SKU {list(KNOWN_SKUS)}", file=sys.stderr)
    key = issue_license(args.email, sku=args.sku, issued=args.issued, expires=args.expires)
    print(key)
    return 0


def _cmd_verify(args: argparse.Namespace) -> int:
    try:
        lic = verify_license(args.key)
    except LicenseError as exc:
        print(f"INVALID — {exc}")
        return 1
    print("VALID")
    print(f"  sku:     {lic.sku}")
    print(f"  email:   {lic.email}")
    print(f"  issued:  {lic.issued}")
    if lic.expires:
        print(f"  expires: {lic.expires}")
    print(f"  premium access: {'yes' if lic.covers_premium() else 'no'}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Issue and verify essay-pipeline license keys")
    sub = parser.add_subparsers(dest="command", required=True)

    p_issue = sub.add_parser("issue", help="Mint a new license key (seller-side)")
    p_issue.add_argument("--email", required=True, help="Buyer email / identity")
    p_issue.add_argument(
        "--sku", default="premium-bundle", help="Product SKU (default: premium-bundle)"
    )
    p_issue.add_argument("--issued", default=None, help="ISO issue date (default: today)")
    p_issue.add_argument(
        "--expires", default=None, help="ISO expiration date for subscription grants"
    )
    p_issue.set_defaults(func=_cmd_issue)

    p_verify = sub.add_parser("verify", help="Verify a license key")
    p_verify.add_argument("--key", required=True, help="License key to verify")
    p_verify.set_defaults(func=_cmd_verify)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()

"""Disposable loopback CA for teaching only. Never distribute generated keys."""
import datetime
import hashlib
import ipaddress
import json
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

from .protocol import atomic_write, require


def create(directory):
    directory = Path(directory)
    require(not directory.exists(), "certificate directory already exists")
    directory.mkdir(parents=True, mode=0o700)
    now = datetime.datetime.now(datetime.timezone.utc)
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "LogBranik disposable lab CA")])
    ca = (x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key())
          .serial_number(x509.random_serial_number()).not_valid_before(now-datetime.timedelta(minutes=1))
          .not_valid_after(now+datetime.timedelta(days=7))
          .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
          .add_extension(x509.KeyUsage(False, False, False, False, False, True, True, False, False), critical=True)
          .sign(key, hashes.SHA256()))
    atomic_write(directory / "ca.crt", ca.public_bytes(serialization.Encoding.PEM))
    fingerprints = {}
    for role in ("agent", "central", "publisher", "collector", "wrong-role"):
        leaf_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        leaf_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, role)])
        usages = [ExtendedKeyUsageOID.SERVER_AUTH] if role in ("agent", "central") else [ExtendedKeyUsageOID.CLIENT_AUTH]
        builder = (x509.CertificateBuilder().subject_name(leaf_name).issuer_name(name)
                   .public_key(leaf_key.public_key()).serial_number(x509.random_serial_number())
                   .not_valid_before(now-datetime.timedelta(minutes=1))
                   .not_valid_after(now+datetime.timedelta(days=7))
                   .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
                   .add_extension(x509.ExtendedKeyUsage(usages), critical=False))
        if role in ("agent", "central"):
            builder = builder.add_extension(x509.SubjectAlternativeName([
                x509.DNSName("localhost"), x509.IPAddress(ipaddress.ip_address("127.0.0.1"))]), critical=False)
        certificate = builder.sign(key, hashes.SHA256())
        atomic_write(directory / f"{role}.crt", certificate.public_bytes(serialization.Encoding.PEM))
        atomic_write(directory / f"{role}.key", leaf_key.private_bytes(serialization.Encoding.PEM,
                     serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
        fingerprints[role] = certificate.fingerprint(hashes.SHA256()).hex()
    # CA private key intentionally not retained: regenerate disposable fixtures.
    atomic_write(directory / "fingerprints.json", json.dumps(fingerprints, indent=2).encode())
    return fingerprints

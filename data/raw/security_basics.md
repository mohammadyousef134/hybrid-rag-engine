# Security Fundamentals

## Encryption

Encryption transforms readable data into an unreadable format using a mathematical algorithm and a key, protecting it from anyone who doesn't hold the correct key. Symmetric encryption uses the same key for both encrypting and decrypting data, making it fast but requiring a secure way to share the key beforehand. Asymmetric encryption uses a pair of keys instead: a public key for encrypting and a private key for decrypting, which solves the key-sharing problem but is computationally slower.

TLS, the protocol behind HTTPS, actually uses both approaches together: asymmetric encryption to securely exchange a temporary key during the initial handshake, then symmetric encryption for the actual data transfer, combining the security benefits of one with the speed of the other.

## Hashing

Hashing converts data into a fixed-length string of characters, but unlike encryption, this process cannot be reversed to recover the original data. Hashing is commonly used to store passwords: instead of saving a user's actual password, a system stores its hash, and compares hashes during login rather than the raw password itself.

A good password hashing algorithm, like bcrypt or Argon2, is deliberately slow to compute, which makes brute-force guessing attacks impractical even if an attacker gains access to the stored hashes. This is different from hashing algorithms used for file integrity checks, like SHA-256, which are designed to be fast.

## Firewalls

A firewall monitors and controls incoming and outgoing network traffic based on a defined set of rules. A network firewall typically filters traffic based on IP addresses and ports, while a web application firewall inspects the actual content of HTTP requests, looking for patterns associated with common attacks like SQL injection or cross-site scripting.

## Common Vulnerabilities

SQL injection occurs when an attacker inserts malicious SQL code into an input field, tricking the application into running unintended database commands. This is typically prevented by using parameterized queries instead of directly inserting user input into a SQL string.

Cross-site scripting, or XSS, happens when an attacker injects malicious scripts into content that's later displayed to other users, allowing the script to run in their browser. Escaping user input before rendering it in HTML is the standard defense against this.

## Zero Trust Architecture

Zero trust is a security model built on the principle of never automatically trusting any request, even one originating from inside the network perimeter. Every request must be authenticated and authorized individually, regardless of where it comes from. This is a shift away from older models that treated anything inside the corporate network as inherently trustworthy.

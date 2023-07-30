# Secure-Email-KDS

Key Distribution Server (KDS) is
needed to allow the distribution of session keys to secure communication over
email using AES-128 encryption. In this schema, a client wishing to send an email (Client A)
to another client (Client B) needs to request a session key from the KDS. Client A and the
KDS connect using TCP whereby Client A sends a specially formatted message to forward
both the sender’s and receiver’s emails to the KDS. The KDS then generates a 128-bit
session key which would be used to encrypt the email contents using AES-128. The KDS
then sends the session key to Client A once encrypted using Client A’s master key and
another encrypted using Client B’s master key. Since Client A has access to their own
master key they are able to decrypt the first encrypted version and retrieve the session key.
Client A then sends the second encrypted version of the session key to Client B, additionally,
they encrypt their email using the session key and send it to Client B. Once Client B receives
the encrypted session key they can decrypt it using their master key. Once the session key
is decrypted it can be used to decrypt the email sent by Client A.

## Demonstration
[![Watch the demonstration video](https://img.youtube.com/vi/NcAn6Of6TR0/maxresdefault.jpg)](https://youtu.be/NcAn6Of6TR0)
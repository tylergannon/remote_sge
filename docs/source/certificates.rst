Certificates
============

SSL is required, and a client-side certificate is required, at the level of
nginx configuration.

http://nategood.com/client-side-certificate-authentication-in-ngi


The following creates all non-encrypted keys, so that passwords
will not be needed.  You might choose to do otherwise.

    openssl genrsa -out ca.key 4096
    
============
Certificates
============

SSL is required, and a client-side certificate is required, at the level of
nginx configuration.

The OpenSSL commands used to create our keys and certificates come courtesy
of `Nate Good`_, with two differences:

* By default, **keys will be unencrypted**.
    * If you're worried about this, see `Encrypted Certificates`_.


.. _`Nate Good`: http://nategood.com/client-side-certificate-authentication-in-ngi

======================
Encrypted Certificates
======================

If you want encrypted certificates, you can set ``enctype = -des3`` when you are
prompted to edit **SSL Settings** during installation.  By doing so you'll be prompted
to give passwords in the appropriate places.  You'll need to modify your nginx config
to specify ssl_password_file_.  See this article_ on stackoverflow for more details.

There is no established pattern for managing the password for the client key.
The :mod:`requests` package has limited support for providing a password for a client
certificate.  See this `github issue`_ for details.  For now if you require a password
for your CA and Server keys, follow the above instructions and then do one of the following:

* Use the client key/cert provided, and then rewrite the key so that it requires no password.
    This process is mentioned in the `github issue`_.  I can't promise that it will work; don't
    know and haven't tested whether rewriting the key will also invalidate the certificate.
* Generate your own password-less key on the client, create a CSR, copy it over to the remote,
    sign it and bring the certificate back to the client.  This much is left up to the user at
    this point.

.. _ssl_password_file: http://nginx.org/en/docs/http/ngx_http_ssl_module.html#ssl_password_file
.. _article: https://stackoverflow.com/questions/33084347/pass-cert-password-to-nginx-with-https-site-during-restart
.. _`github issue`: https://github.com/requests/requests/issues/1573

===========================================
Installing a proper TLS Cert for the server
===========================================

The CSR generated by the installer will be left in the ``certs`` directory under your
configuration root, and can be submitted to the proper authority for a verifiable
certificate.  *Note that this is only needed if you're worried about DNS spoofing.*

An easy alternative is to always use the IP address of the remote in your client
configuration, which would be much more difficult to spoof.


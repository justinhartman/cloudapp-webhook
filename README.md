# Creative Academy CloudApp/Drive Webhook

This project creates a webhook for [CloudApp][cloudapp] to upload video and
images to the [Creative Academy][ctca] Google Drive API.

## License

Copyright (c) 2020, Cape Town Creative Academy (Pty) Limited.

This project is licensed under copyright protection and details of which are
contained in the [LICENSE][license] file.

## Gandi Python

### Install Packages for Google Drive API

```console
$ /home/hosting-user/.local/bin/pip3 --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

```console
$ ls -lha /home/hosting-user/.local/bin/
chardetect
easy_install
easy_install-3.5
google-oauthlib-tool
pip
pip3
pip3.5
pyrsa-decrypt
pyrsa-encrypt
pyrsa-keygen
pyrsa-priv2pub
pyrsa-sign
pyrsa-verify
wheel
```

```console
$ ls -lha /home/hosting-user/.local/lib/python3.5/site-packages/
apiclient
cachetools
cachetools-4.0.0.dist-info
certifi
certifi-2020.4.5.1.dist-info
chardet
chardet-3.0.4.dist-info
easy_install.py
google
google_api_core-1.16.0-py3.8-nspkg.pth
google_api_core-1.16.0.dist-info
google_api_python_client-1.8.0.dist-info
google_auth-1.13.1-py3.8-nspkg.pth
google_auth-1.13.1.dist-info
google_auth_httplib2-0.0.3.dist-info
google_auth_httplib2.py
google_auth_oauthlib
google_auth_oauthlib-0.4.1.dist-info
googleapiclient
googleapis_common_protos-1.51.0-py3.5-nspkg.pth
googleapis_common_protos-1.51.0.dist-info
httplib2
httplib2-0.17.1.dist-info
idna
idna-2.9.dist-info
oauthlib
oauthlib-3.1.0.dist-info
pip
pip-20.0.2.dist-info
pkg_resources
protobuf-3.11.3-py3.5-nspkg.pth
protobuf-3.11.3.dist-info
pyasn1
pyasn1-0.4.8.dist-info
pyasn1_modules
pyasn1_modules-0.2.8.dist-info
pytz
pytz-2019.3.dist-info
requests
requests-2.23.0.dist-info
requests_oauthlib
requests_oauthlib-1.3.0.dist-info
rsa
rsa-4.0.dist-info
setuptools
setuptools-46.1.3.dist-info
six-1.14.0.dist-info
six.py
uritemplate
uritemplate-3.0.1.dist-info
urllib3
urllib3-1.25.8.dist-info
wheel
wheel-0.34.2.dist-info
```

[cloudapp]: https://getcloudapp.com
[ctca]: https://creativeacademy.ac.za
[license]: LICENSE

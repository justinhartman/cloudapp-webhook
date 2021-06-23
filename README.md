# CloudApp/Google Drive Webhook on Heroku

This project creates a webhook for [CloudApp][cloudapp] to upload video and
images to a company Google Workspace Google Drive API running on a Heroku
Python server.

## Install

### Virtual Environment

```console
$ pipenv run python3 -m pip install --upgrade pip
$ pipenv install
$ pipenv sync --sequential
```

### Shell Envrionment

```console
$ pipenv shell
```

Optionally, run a command without being in shell:

```console
$ pipenv run [OPTIONS] COMMAND [ARGS]
```

End session:

```console
$ deactivate
```

## Configuration

There is a [`settings.py`][settings] file which contains all the configuration
settings you may need. Please go through this file and change these settings
to your environment.

### CloudApp

You will need a paid [CloudApp][cloudapp] account in order to use this webhook.
Within CloudApp you will also need to configure a custom domain and endpoint
which will need to be configured in the `settings.py` file where you see the
[HTTP_URL][appurl] environment setting.

### Heroku

This application is set up to work with a [Heroku][heroku] virtual server and
you will need to add your Google Drive API details to the
[`heroku.json` file here][heroku-config].

### Using rclone

If you're going to use `rclone` be sure to change your Team Drive ID
(`team_drive`) in the `rclone.conf` file.

## Deployment

Deployment to a Heroku server is out scope for this README and you will
need to set up and configure your own workflow and pipelines in Heroku.

I do use a [Fabric][fabric] file which you'll find at `./fabfile.py` for
deployments to GitHub, and Heroku, using Heroku Git. You can work off this file
to configure your own deployments to Heroku.

### Heroku Buildpacks

When you do configure your server in Heroku you will need to add two buildpacks
to your server. Click on **Settings** within your app
(e.g. `https://dashboard.heroku.com/apps/cloudapp-python/settings`) and scroll
down to the Buildpacks section.

Click the **Add buildpack** button and add these two buildpacks:

1. `heroku/python`
2. `https://github.com/22digital/heroku-gdrive-buildpack.git`

The second buildpack [found at 22 Digital][buildpack] has been
tailored and customised to work with this app. This buildpack
will install all the dependencies you need on Heroku.

## Webhook Endpoint

The webhook endpoint is configured to be the domain you set in `settings.py` as
your `HTTP_URL` and the endpoint only accepts a `POST` request.

Consider the following `cURL` request:

```
curl -X POST --location "https://cloudapp-python.herokuapp.com" \
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{
            \"event\": \"post\",
            \"payload\": {
                \"item_name\": \"Test Image\",
                \"item_url\": \"https://cloudapp.com/image.jpg\",
                \"created_at\": \"2021-06-22 22:22:22\"
            }
        }"
```

CloudApp will send a `POST` request to `https://cloudapp-python.herokuapp.com`
and it should always contain the `event` and `payload` properties. The app will
use these and save the `event`, `item_name`, `item_url`, and `created_at` in the
SQLite database and return a `success` message with a `200` response code.

```
HTTP/1.1 200 OK
Connection: keep-alive
Server: nginx
Date: Wed, 23 Jun 2021 23:18:27 GMT
Content-Type: application/json
Transfer-Encoding: chunked
Via: 1.1 vegur

{
  "event": "success",
  "code": 200,
  "payload": {
    "id": "207",
    "item_name": "Test Image",
    "item_url": "https:\/\/cloudapp.com\/image.jpg"
  }
}

Response code: 200 (OK); Time: 1890ms; Content length: 125 bytes
```

The app will also send out an email to the email address configured in
`settings.py` confirming the new media upload.

## License

Copyright (c) 2020-2021, Justin Hartman <https://justinhartman.co>.

This project is licensed under an [`MIT`][mit] and details can be found in the
[LICENSE][license] file.


[heroku]: https://heroku.com
[fabric]: https://getfabric.com
[cloudapp]: https://getcloudapp.com
[license]: LICENSE
[mit]: https://opensource.org/licenses/MIT
[buildpack]: https://github.com/22digital/heroku-gdrive-buildpack
[settings]: https://github.com/justinhartman/cloudapp-webhook/blob/master/settings.py
[appurl]: https://github.com/justinhartman/cloudapp-webhook/blob/master/settings.py#L34
[heroku-config]: https://github.com/justinhartman/cloudapp-webhook/blob/master/.config/heroku.json

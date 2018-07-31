# epochron

[![Build Status](https://travis-ci.org/robertjkeck2/epochron.svg?branch=master)](https://travis-ci.org/robertjkeck2/epochron)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

REST ful Webcron Service with Webhooks. Check out the project's [documentation](http://robertjkeck2.github.io/epochron/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  
- [Travis CLI](http://blog.travis-ci.com/2013-01-14-new-client/)
- [Heroku Toolbelt](https://toolbelt.heroku.com/)

# Initialize the project

Start the dev server for local development:

```bash
docker-compose up
```

Create a superuser to login to the admin:

```bash
docker-compose run --rm web ./manage.py createsuperuser
```


# Continuous Deployment

Deployment automated via Travis. When builds pass on the master or qa branch, Travis will deploy that branch to Heroku. Enable this by:

Creating the production sever:

```
heroku create epochron-prod --remote prod && \
    heroku addons:create newrelic:wayne --app epochron-prod && \
    heroku addons:create heroku-postgresql:hobby-dev --app epochron-prod && \
    heroku config:set DJANGO_SECRET=`openssl rand -base64 32` \
        DJANGO_AWS_ACCESS_KEY_ID="Add your id" \
        DJANGO_AWS_SECRET_ACCESS_KEY="Add your key" \
        DJANGO_AWS_STORAGE_BUCKET_NAME="epochron-prod" \
        --app epochron-prod
```

Creating the qa sever:

```
heroku create `epochron-qa --remote qa && \
    heroku addons:create newrelic:wayne && \
    heroku addons:create heroku-postgresql:hobby-dev && \
    heroku config:set DJANGO_SECRET=`openssl rand -base64 32` \
        DJANGO_AWS_ACCESS_KEY_ID="Add your id" \
        DJANGO_AWS_SECRET_ACCESS_KEY="Add your key" \
        DJANGO_AWS_STORAGE_BUCKET_NAME="epochron-qa" \
```

Securely add your heroku credentials to travis so it can automatically deploy your changes.

```bash
travis encrypt HEROKU_AUTH_TOKEN="$(heroku auth:token)" --add
```

Commit your changes and push to master and qa to trigger your first deploys:

```bash
git commit -m "ci(travis): added heroku credentials" && \
git push origin master && \
git checkout -b qa && \
git push -u origin qa
```
You're ready to continuously ship! ✨ 💅 🛳

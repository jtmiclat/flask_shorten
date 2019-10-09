# An example of a Flask Url Shortener
![build](https://gitlab.com/jtcmic/flask_shorten/badges/master/pipeline.svg)

## Deployed example

This app is deployed in Digital Ocean. App can be located at [here](https://link.jtmiclat.me/). The website was meant as an example on how deploy the app and not be used as a real service. I do not guarantee that the data will always be persisted and be accurate.

### CI/CD
Uses gitlab for CI.

## Design decisions

Used postgres as an easy to use database but it might better to use something
like redis or document models for faster lookup.

Used `flask-rest-api` as it is my preferred choice for creating simple RESTApis.


## Quick Start Guide
Posting a auto generate a code
```
curl -X POST http://0.0.0.0:5000/urlmapping -H "Content-type: application/json" -d '{"url":"http://jtmiclat.com"}'
```
Returns Something like
```
{
  "new_url": "d3WQrwzG", 
  "url": "http://jtmiclat.com"
}
```

You can then access it via
```
curl http://0.0.0.0:5000/d3WQrwzG
```
Redirects to
```
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to target URL: <a href="http://jtmiclat.com">http://jtmiclat.com</a>.  If not click the link
```



# An example of a Flask Url Shortener

## TODO

[ ] Deploy this to digital ocean via kubernetes or kubeless
[ ] Bunch of tests
[ ] Add documentation

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

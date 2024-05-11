# SearXNG
SearXNG is a free internet metasearch engine which aggregates results from various search services and databases. Users are neither tracked nor profiled. Dify has implemented the interface to access the SearXNG, so you can use it directly in Dify. followings are steps to integrate SearXNG in Dify.

## 1. Install SearXNG using Docker
```
docker run --rm \
             -d -p 8080:8080 \
             -v "${PWD}/searxng:/etc/searxng" \
             -e "BASE_URL=http://0.0.0.0:8080/" \
             -e "INSTANCE_NAME=searxng" \
             searxng/searxng
```
If you intend to install SearXNG using alternative methods. Please refer to [this page](https://docs.searxng.org/admin/installation.html).

## 2. Change settings.yml
When you install SearxNG, the default output format is the HTML format. You need to activate the json format. Add the following line to the settings.yml file. The settings.yml file is located at ${PWD}/searxng/settings.yml, as demonstrated in the previous example.
```
  # remove format to deny access, use lower case.
  # formats: [html, csv, json, rss]
  formats:
    - html
    - json    # <-- add this line 
```

## 3. Integrate SearXNG in Dify
Fill in the base url http://x.x.x.x:8080 in `Tools > SearXNG > To Authorize` page to active it.

## 4. Finish
Have a fun!


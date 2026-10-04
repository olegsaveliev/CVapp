#!/bin/sh
# Wraps cv-site.html into a full standalone page at site/index.html
cd "$(dirname "$0")"
{ printf '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta property="og:title" content="Oleg Saveliev · Senior Delivery Manager, AI/ML & GenAI">\n<meta property="og:description" content="19 years in IT. AI/ML and GenAI program delivery. Kyiv, Ukraine.">\n<meta name="theme-color" content="#EEF2F5">\n</head>\n<body>\n'; cat cv-site.html; printf '\n</body>\n</html>\n'; } > site/index.html

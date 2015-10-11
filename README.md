# django-babeljs #
A simple interface to babel.js: transpile your javascript template into a javascript tag.

## install ##
Just include `babeljs` into your `INSTALLED_APPS`
```
#!python

INSTALLED_APPS += [ "babeljs" ]
```


## templatetag ##

Load the templatetag
```
#!html
{% load babeljs %}
```

### babeljs ###
Include the babeljs file(s) as `<scrip...></script>` tag(s).
It is useful only for in browser transpilation (ie: no nodejs is installed), otherwise can be omitted
```
#!html
{% babeljs %}
```

### babel ###
load file.js, try to transpile it with babeljs and copy the result into the template (acts the same as the `include` tag)
```
#!html
{% babel "file.js" %}
```

transpile a react jsx file
```
#!html
{% babel "file.jsx" %}
```


## settings ##

### BABELJS_BABEL ###
Provide a custom babeljs script.

### BABELJS_ROOT ###
Where to find the babeljs script.

### BABELJS_MINIFIED ###
If use or not the minified version [default=not DEBUG].
Useful only for default babeljs script.

### BABELJS_CACHE_BACKEND ###
Use a specific cache backend for compiled js [default="default"].

### BABELJS_CACHE_TIMEOUT ###
The number of seconds the transpiled code should be stored in the cache, 0 for never cache it, None for cache it forever [default=300].

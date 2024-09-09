## myapi [![pypi version][1]][2] [![paypal donation][3]][4]

[![license][5]][6] [![python version][7]][8] [![django version][9]][10] [![build][11]][12] [![black][18]][19]

**myapi** is a Markdown Editor plugin for Django, supported for _Bootstrap_ & _Semantic-UI_.


### Features

* Live Preview
* Integrated with [_Ace Editor_](https://ace.c9.io)
* Supported with [_Bootstrap_](https://getbootstrap.com) and [_Semantic-UI_](https://semantic-ui.com)
* Supported Multiple Fields [_fixed this issue_](https://github.com/agusmakmun/django-markdown-editor/issues/3)
* Upload Images to imgur.com _(via API)_ and [custom uploader][13]
* Direct Mention users `@[username]` - _(requires user to logged in)_.
* Supports embed/iframe video from (Youtube, Vimeo, Dailymotion, Yahoo, Veoh, & Metacafe)
* Spellchecking (only supports US English at this time)
* Emoji `:emoji_name:` + Cheat sheets
* myapi Commands Reference
* Supports Django Admin
* Toolbar Buttons
* Highlight `pre`


### Preview

![editor](https://raw.githubusercontent.com/agusmakmun/django-markdown-editor/master/.etc/images/bootstrap/myapi-editor.png)

![preview](https://raw.githubusercontent.com/agusmakmun/django-markdown-editor/master/.etc/images/bootstrap/myapi-preview.png)


### Requirements

* `Django>=3.2`
* `Markdown>=3.0`
* `requests>=2.12.4`
* `bleach`


### Installation

myapi is available directly from [PyPI][2]:

**1.** Installing the package.

```
$ pip install myapi
```


**2.** Don't forget to add `'myapi'` to your `'INSTALLED_APPS'` setting _(without migrations)_.

```python
# settings.py
INSTALLED_APPS = [
    ....
    'myapi',
]
```


**3.** Add url pattern to your `urls.py.`

```python
# urls.py
urlpatterns = [
    ...
    path('api/', include('myapi.urls')),
]
```


**4.** Collect myapi's static files in your `STATIC_ROOT` folder.

```
./manage.py collectstatic
```


### Setting Configurations `settings.py`

Please register your application at https://api.imgur.com/oauth2/addclient
to get `IMGUR_CLIENT_ID` and `IMGUR_API_KEY`.

```python
# Choices are: "semantic", "bootstrap"
myapi_THEME = 'bootstrap'

# Global myapi settings
# Input: string boolean, `true/false`
myapi_ENABLE_CONFIGS = {
    'emoji': 'true',        # to enable/disable emoji icons.
    'imgur': 'true',        # to enable/disable imgur/custom uploader.
    'mention': 'false',     # to enable/disable mention
    'jquery': 'true',       # to include/revoke jquery (require for admin default django)
    'living': 'false',      # to enable/disable live updates in preview
    'spellcheck': 'false',  # to enable/disable spellcheck in form textareas
    'hljs': 'true',         # to enable/disable hljs highlighting in preview
}

# To show the toolbar buttons
myapi_TOOLBAR_BUTTONS = [
    'bold', 'italic', 'horizontal', 'heading', 'pre-code',
    'blockquote', 'unordered-list', 'ordered-list',
    'link', 'image-link', 'image-upload', 'emoji',
    'direct-mention', 'toggle-maximize', 'help'
]

# To setup the myapi editor with title label or not (default is False)
myapi_ENABLE_LABEL = False

# Imgur API Keys
myapi_IMGUR_CLIENT_ID = 'your-client-id'
myapi_IMGUR_API_KEY   = 'your-api-key'

# Markdownify
myapi_MARKDOWNIFY_FUNCTION = 'myapi.utils.markdownify' # default
myapi_MARKDOWNIFY_URL = '/myapi/markdownify/' # default

# Delay in miliseconds to update editor preview when in living mode.
myapi_MARKDOWNIFY_TIMEOUT = 0 # update the preview instantly
# or:
myapi_MARKDOWNIFY_TIMEOUT = 1000 # default

# Markdown extensions (default)
myapi_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.nl2br',
    'markdown.extensions.smarty',
    'markdown.extensions.fenced_code',

    # Custom markdown extensions.
    'myapi.extensions.urlize',
    'myapi.extensions.del_ins',      # ~~strikethrough~~ and ++underscores++
    'myapi.extensions.mention',      # to parse markdown mention
    'myapi.extensions.emoji',        # to parse markdown emoji
    'myapi.extensions.mdx_video',    # to parse embed/iframe video
    'myapi.extensions.escape_html',  # to handle the XSS vulnerabilities
]

# Markdown Extensions Configs
myapi_MARKDOWN_EXTENSION_CONFIGS = {}

# Markdown urls
myapi_UPLOAD_URL = '' # Completely disable the endpoint
# or:
myapi_UPLOAD_URL = '/myapi/uploader/' # default

myapi_SEARCH_USERS_URL = '' # Completely disables the endpoint
# or:
myapi_SEARCH_USERS_URL = '/myapi/search-user/' # default

# Markdown Extensions
# myapi_MARKDOWN_BASE_EMOJI_URL = 'https://www.webfx.com/tools/emoji-cheat-sheet/graphics/emojis/'     # from webfx
myapi_MARKDOWN_BASE_EMOJI_URL = 'https://github.githubassets.com/images/icons/emoji/'                  # default from github
# or:
myapi_MARKDOWN_BASE_EMOJI_URL = ''  # Completely disables the endpoint
myapi_MARKDOWN_BASE_MENTION_URL = 'https://python.web.id/author/'                                      # please change this to your domain

# If you need to use your own themed "bootstrap" or "semantic ui" dependency
# replace the values with the file in your static files dir
myapi_ALTERNATIVE_JS_FILE_THEME = "semantic-themed/semantic.min.js"   # default None
myapi_ALTERNATIVE_CSS_FILE_THEME = "semantic-themed/semantic.min.css" # default None
myapi_ALTERNATIVE_JQUERY_JS_FILE = "jquery/dist/jquery.min.js"        # default None

# URL schemes that are allowed within links
ALLOWED_URL_SCHEMES = [
    "file", "ftp", "ftps", "http", "https", "irc", "mailto",
    "sftp", "ssh", "tel", "telnet", "tftp", "vnc", "xmpp",
]

# https://gist.github.com/mrmrs/7650266
ALLOWED_HTML_TAGS = [
    "a", "abbr", "b", "blockquote", "br", "cite", "code", "command",
    "dd", "del", "dl", "dt", "em", "fieldset", "h1", "h2", "h3", "h4", "h5", "h6",
    "hr", "i", "iframe", "img", "input", "ins", "kbd", "label", "legend",
    "li", "ol", "optgroup", "option", "p", "pre", "small", "span", "strong",
    "sub", "sup", "table", "tbody", "td", "tfoot", "th", "thead", "tr", "u", "ul"
]

# https://github.com/decal/werdlists/blob/master/html-words/html-attributes-list.txt
ALLOWED_HTML_ATTRIBUTES = [
    "alt", "class", "color", "colspan", "datetime",  # "data",
    "height", "href", "id", "name", "reversed", "rowspan",
    "scope", "src", "style", "title", "type", "width"
]
```

Check this setting is not set else csrf will not be sent over ajax calls:

```python
CSRF_COOKIE_HTTPONLY = False
```


### Usage


#### Model

```python
from django.db import models
from myapi.models import myapiField

class Post(models.Model):
    description = myapiField()
```


#### Form

```python
from django import forms
from myapi.fields import myapiFormField

class PostForm(forms.Form):
    description = myapiFormField()
```


#### Admin

```python
from django.db import models
from django.contrib import admin

from myapi.widgets import AdminmyapiWidget

from yourapp.models import YourModel

class YourModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminmyapiWidget},
    }

admin.site.register(YourModel, YourModelAdmin)
```


#### Template Renderer

Simply safely parse markdown content as html ouput by loading templatetags from `myapi/templatetags/myapitags.py`.

```html
{% load myapitags %}
{{ field_name|safe_markdown }}

# example
{{ post.description|safe_markdown }}
```


Don't miss to include the required css & js files before use.
You can take a look at this folder [myapi_demo/app/templates][14] for more details.
The below example is a one of the way to implement it when you choose the `myapi_THEME = 'bootstrap'`:

```html
{% extends "bootstrap/base.html" %}
{% load static %}
{% load myapitags %}

{% block css %}
  <link href="{% static 'plugins/css/ace.min.css' %}" type="text/css" media="all" rel="stylesheet" />
  <link href="{% static 'myapi/css/myapi.bootstrap.min.css' %}" type="text/css" media="all" rel="stylesheet" />
{% endblock %}

{% block content %}
  <div class="myapi-preview">
    <h1>Title: {{ post.title }}</h1>
    <p><b>Description:</b></p>
    <hr />
    {{ post.description|safe_markdown }}
  </div>
{% endblock %}

{% block js %}
  <script type="text/javascript" src="{% static 'plugins/js/highlight.min.js' %}"></script>
  <script>
    $('.myapi-preview pre').each(function(i, block){
        hljs.highlightBlock(block);
    });
  </script>
{% endblock %}
```


#### Template Editor Form

Different with *Template Renderer*, the *Template Editor Form* have more css & javascript dependencies.

```html
{% extends "bootstrap/base.html" %}
{% load static %}

{% block css %}
  <link href="{% static 'plugins/css/ace.min.css' %}" type="text/css" media="all" rel="stylesheet" />
  <link href="{% static 'plugins/css/resizable.min.css' %}" type="text/css" media="all" rel="stylesheet" />
  <link href="{% static 'myapi/css/myapi.bootstrap.min.css' %}" type="text/css" media="all" rel="stylesheet" />
{% endblock %}

{% block content %}
  <form class="form" method="post">{% csrf_token %}
    <div class="form-group">
      {{ form.title }}
    </div>
    <div class="form-group">
      {{ form.description }}
    </div>
    <div class="form-group">
      <button class="btn btn-success">
        <i class="save icon"></i> Save Post
      </button>
    </div>
  </form>
{% endblock %}

{% block js %}
  <script type="text/javascript" src="{% static 'plugins/js/ace.js' %}"></script>
  <script type="text/javascript" src="{% static 'plugins/js/mode-markdown.js' %}"></script>
  <script type="text/javascript" src="{% static 'plugins/js/ext-language_tools.js' %}"></script>
  <script type="text/javascript" src="{% static 'plugins/js/theme-github.js' %}"></script>
  <script type="text/javascript" src="{% static 'plugins/js/typo.js' %}"></script>
  <script type="text/javascript" src="{% static 'plugins/js/spellcheck.js' %}"></script>
  <script type="text/javascript" src="{% static 'plugins/js/highlight.min.js' %}"></script>
  <script type="text/javascript" src="{% static 'plugins/js/resizable.min.js' %}"></script>
  <script type="text/javascript" src="{% static 'plugins/js/emojis.min.js' %}"></script>
  <script type="text/javascript" src="{% static 'myapi/js/myapi.bootstrap.min.js' %}"></script>
{% endblock %}
```


### Custom Uploader

If you want to save the images uploaded to your storage,
**myapi** also provides a way to handle this. Please checkout this [WIKI][13]


### Test myapi from this Repository

Assuming you are already setup with a virtual enviroment (virtualenv):

```
$ git clone https://github.com/agusmakmun/django-markdown-editor.git
$ cd django-markdown-editor/ && python setup.py install
$ cd myapi_demo/
$ python manage.py makemigrations && python manage.py migrate
$ python manage.py runserver
```


Checkout at http://127.0.0.1:8000/simple-form/ on your browser.


### myapi Commands Reference

![command refference](https://raw.githubusercontent.com/agusmakmun/django-markdown-editor/master/.etc/images/bootstrap/myapi-guide.png)


### Notes

**myapi** was inspired by these great projects: [django-markdownx][15], [Python Markdown][16] and [Online reStructuredText editor][17].


[1]: https://img.shields.io/pypi/v/myapi.svg
[2]: https://pypi.python.org/pypi/myapi

[3]: https://img.shields.io/badge/donate-paypal-blue
[4]: https://www.paypal.com/paypalme/summonagus

[5]: https://img.shields.io/badge/license-GNUGPLv3-blue.svg
[6]: https://raw.githubusercontent.com/agusmakmun/django-markdown-editor/master/LICENSE

[7]: https://img.shields.io/pypi/pyversions/myapi.svg
[8]: https://pypi.python.org/pypi/myapi

[9]: https://img.shields.io/badge/Django-3.2%20%3E=%204.1-green.svg
[10]: https://www.djangoproject.com

[11]: https://img.shields.io/github/actions/workflow/status/agusmakmun/django-markdown-editor/run-tests.yml?branch=master
[12]: https://github.com/agusmakmun/django-markdown-editor/actions/workflows/run-tests.yml

[13]: https://github.com/agusmakmun/django-markdown-editor/wiki
[14]: https://github.com/agusmakmun/django-markdown-editor/tree/master/myapi_demo/app/templates
[15]: https://github.com/adi-/django-markdownx
[16]: https://github.com/waylan/Python-Markdown
[17]: http://rst.ninjs.org

[18]: https://img.shields.io/badge/code%20style-black-000000.svg
[19]: https://github.com/ambv/black

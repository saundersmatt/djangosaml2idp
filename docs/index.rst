:Release: 0.1.11
:Date: 12/03/2017

Welcome to djangosaml2idp's documentation!
==========================================

djangosaml2idp
===============

.. image:: https://travis-ci.org/mhindery/djangosaml2idp.svg?branch=master
    :target: https://travis-ci.org/mhindery/djangosaml2idp
    :alt: Travis CI

.. image:: https://landscape.io/github/mhindery/djangosaml2idp/master/landscape.svg?style=flat
   :target: https://landscape.io/github/mhindery/djangosaml2idp/master
   :alt: Code Health

.. image:: https://lima.codeclimate.com/github/mhindery/djangosaml2idp/badges/gpa.svg
   :target: https://lima.codeclimate.com/github/mhindery/djangosaml2idp
   :alt: Code Climate

.. image:: https://requires.io/github/mhindery/djangosaml2idp/requirements.svg?branch=master
     :target: https://requires.io/github/mhindery/djangosaml2idp/requirements/?branch=master
     :alt: Requirements Status


djangosaml2idp implements the Identity Provider side of the SAML2 protocol with Django.
It builds on top of PySAML2_, is compatible with Python 2/3 and all current supported Django versions.

.. _PySAML2: https://github.com/rohe/pysaml2/

Installation
------------

PySAML2 uses xmlsec1_ binary to sign SAML assertions so you need to install
it either through your operating system package or by compiling the source
code. It doesn't matter where the final executable is installed because
you will need to set the full path to it in the configuration stage.
``xmlsec`` is available (at least) for Debian, OSX and Alpine Linux.

.. _xmlsec1: http://www.aleksey.com/xmlsec/

Now you can install the djangosaml2idp package using pip. This
will also install PySAML2 and its dependencies automatically::

    pip install djangosaml2idp


Configuration & Usage
---------------------
The first thing you need to do is add ``djangosaml2idp`` to the list of installed apps::

  INSTALLED_APPS = (
      'django.contrib.admin',
      'djangosaml2idp',
      ...
  )

Now include ``djangosaml2idp`` in your project by adding it in the url config::

    from django.conf.urls import url, include
    from django.contrib import admin

    urlpatterns = [
        url(r'^idp/', include('djangosaml2idp.urls')),
        url(r'^admin/', admin.site.urls),
        ...
    ]

In your Django settings, configure your IdP. Configuration follows the pysaml2_configuration_. The IdP from the example project looks like this::

    ...
    import saml2
    from saml2.saml import NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED
    from saml2.sigver import get_xmlsec_binary

    BASE_URL = "http://localhost:9000/idp"

    SAML_IDP_CONFIG = {
        "entityid": "%s/metadata" % BASE_URL,
        "description": "Example IdP setup",
        "valid_for": 168,
        "service": {
            "idp": {
                "name": "Django localhost IdP",
                "endpoints": {
                    "single_sign_on_service": [
                        ("%s/sso/post" % BASE_URL, saml2.BINDING_HTTP_POST),
                        ("%s/sso/redirect" % BASE_URL, saml2.BINDING_HTTP_REDIRECT),
                    ],
                },
                "name_id_format": [NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED],
                'sign_response': True,
                'sign_assertion': True,
            },
        },
        'metadata': {
            'local': [os.path.join(os.path.join(os.path.join(BASE_DIR, 'idp'), 'saml2_config'), 'sp_metadata.xml')],
        },
        # Signing
        'key_file': BASE_DIR + '/certificates/private_key.pem',  # private part
        'cert_file': BASE_DIR + '/certificates/public_key.pem',  # public part
        # Encryption
        'encryption_keypairs': [{
            'key_file': BASE_DIR + '/certificates/private_key.pem',  # private part
            'cert_file': BASE_DIR + '/certificates/public_key.pem',  # public part
        }],
        "xmlsec_binary": get_xmlsec_binary(["/opt/local/bin", "/usr/bin/xmlsec1"]),
        'debug' : DEBUG,
    }

You also have to define a mapping for each SP you talk to::

    SAML_IDP_ACS_ATTRIBUTE_MAPPING = {
        "http://localhost:8000/saml2/metadata/": {
            # Map Django user attributes to output SAML attributes
            'email': 'email',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'is_staff': 'is_staff',
            'is_superuser':  'is_superuser',
        }
    }

That's all for the IdP configuration. Assuming you run the Django development server on localhost:8000, you can get its metadata by visiting http://localhost:8000/idp/metadata/.
Use this metadata xml to configure your SP. Place the metadata xml from that SP in the location specified in the config dict (sp_metadata.xml in the example above).

.. _pysaml2_configuration: https://github.com/rohe/pysaml2/blob/master/doc/howto/config.rst

Example project
---------------
``example_project`` contains a barebone demo setup.
It consists of a Service Provider implemented with ``djangosaml2`` and an Identity Provider using ``djangosaml2idp``.


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
=========
Analytics
=========

D-BAS uses `Matomo <https://matomo.org/>`_ as free and open source analytics platform. However the last 16 Bit of each IP are masked.

Matomos URL has to be hardcoded in:
 - `dbas/templates/imprint.pt`
 - `dbas/templates/basetemplate.pt`

First template containts the opt-out plugin of Piwik. Second template contains the tracking frame.

Useful Links for the Geo-IP-Plugin
----------------------------------
- http://matomo.org/faq/how-to/faq_166/
- http://matomo.org/faq/how-to/#faq_163
- http://nginx.org/en/docs/http/ngx_http_geoip_module.html
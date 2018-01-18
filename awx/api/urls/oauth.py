# Copyright (c) 2017 Ansible, Inc.
# All Rights Reserved.

from django.conf.urls import url, include

from oauth2_provider.urls import base_urlpatterns

from awx.api.views import (
    ApiOAuthAuthorizationRootView,
)

from .user_oauth import urls as user_oauth_urls

urls = [
    url(r'^me/oauth/', include(user_oauth_urls)),
    url(r'^$', ApiOAuthAuthorizationRootView.as_view(), name='oauth_authorization_root_view'),
] + base_urlpatterns


__all__ = ['urls']

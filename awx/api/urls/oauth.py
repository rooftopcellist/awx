# Copyright (c) 2017 Ansible, Inc.
# All Rights Reserved.

from django.conf.urls import url, include

from oauth2_provider.urls import base_urlpatterns

from awx.api.views import (
    ApiOAuthAuthorizationRootView,
    UserMeOauthApplicationList,
    UserMeOauthApplicationDetail,
    UserMeOauthApplicationTokenList,
    UserMeOauthApplicationActivityStreamList,
)


urls = [
    url(r'^applications/$', UserMeOauthApplicationList.as_view(), name='user_me_oauth_application_list'),
    url(
        r'^applications/(?P<pk>[0-9]+)/$',
        UserMeOauthApplicationDetail.as_view(),
        name='user_me_oauth_application_detail'
    ),
    url(
        r'^applications/(?P<pk>[0-9]+)/tokens/$',
        UserMeOauthApplicationTokenList.as_view(),
        name='user_me_oauth_application_token_list'
    ),
    url(
        r'^applications/(?P<pk>[0-9]+)/activity_stream/$',
        UserMeOauthApplicationActivityStreamList.as_view(),
        name='user_me_oauth_application_activity_stream_list'
    ),
    url(r'^$', ApiOAuthAuthorizationRootView.as_view(), name='oauth_authorization_root_view'),
] + base_urlpatterns


__all__ = ['urls']

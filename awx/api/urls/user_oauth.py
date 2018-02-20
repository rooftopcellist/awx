# Copyright (c) 2017 Ansible, Inc.
# All Rights Reserved.

from django.conf.urls import url

from awx.api.views import (
    OAuth2RootView,
    UserMeOauthApplicationList,
    OAuth2ApplicationDetail,
    UserMeOauthApplicationTokenList,
    UserMeOauthApplicationActivityStreamList,
    UserMeOauthTokenList,
    UserMeOauthTokenDetail,
    UserMeOauthTokenActivityStreamList,
    UserMeOAuth2PersonalTokenList
)


urls = [
    url(r'^$', OAuth2RootView.as_view(), name='o_auth2_root_view'),
    url(r'^applications/$', UserMeOauthApplicationList.as_view(), name='user_me_oauth_application_list'),
    url(
        r'^applications/(?P<pk>[0-9]+)/$',
        OAuth2ApplicationDetail.as_view(),
        name='o_auth2_application_detail'
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
    url(r'^tokens/$', UserMeOauthTokenList.as_view(), name='user_me_oauth_token_list'),
    url(
        r'^tokens/(?P<pk>[0-9]+)/$',
        UserMeOauthTokenDetail.as_view(),
        name='user_me_oauth_token_detail'
    ),
    url(
        r'^tokens/(?P<pk>[0-9]+)/activity_stream/$',
        UserMeOauthTokenActivityStreamList.as_view(),
        name='user_me_oauth_token_activity_stream_list'
    ),
    url(r'^personal_tokens/$', UserMeOAuth2PersonalTokenList.as_view(), name='user_me_o_auth2_personal_token_list'),    
]

__all__ = ['urls']
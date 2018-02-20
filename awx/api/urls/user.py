# Copyright (c) 2017 Ansible, Inc.
# All Rights Reserved.

from django.conf.urls import url, include

from awx.api.views import (
    UserList,
    UserDetail,
    UserTeamsList,
    UserOrganizationsList,
    UserAdminOfOrganizationsList,
    UserProjectsList,
    UserCredentialsList,
    UserRolesList,
    UserActivityStreamList,
    UserAccessList,
    UserMeOauthApplicationList,
    OAuth2RootView,
    UserMeOauthTokenList,
    UserMeOAuth2AuthorizedTokenList,
    UserMeOAuth2PersonalTokenList
)

from .user_oauth import urls as user_oauth_urls

urls = [ 
    url(r'^$', UserList.as_view(), name='user_list'),
    url(r'^(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user_detail'),
    url(r'^(?P<pk>[0-9]+)/teams/$', UserTeamsList.as_view(), name='user_teams_list'),
    url(r'^(?P<pk>[0-9]+)/organizations/$', UserOrganizationsList.as_view(), name='user_organizations_list'),
    url(r'^(?P<pk>[0-9]+)/admin_of_organizations/$', UserAdminOfOrganizationsList.as_view(), name='user_admin_of_organizations_list'),
    url(r'^(?P<pk>[0-9]+)/projects/$', UserProjectsList.as_view(), name='user_projects_list'),
    url(r'^(?P<pk>[0-9]+)/credentials/$', UserCredentialsList.as_view(), name='user_credentials_list'),
    url(r'^(?P<pk>[0-9]+)/roles/$', UserRolesList.as_view(), name='user_roles_list'),
    url(r'^(?P<pk>[0-9]+)/activity_stream/$', UserActivityStreamList.as_view(), name='user_activity_stream_list'),
    url(r'^(?P<pk>[0-9]+)/access_list/$', UserAccessList.as_view(), name='user_access_list'),
    url(r'^(?P<pk>[0-9]+)/applications/$', UserMeOauthApplicationList.as_view(), name='user_me_oauth_application_list'),
    url(r'^(?P<pk>[0-9]+)/tokens/$', UserMeOauthTokenList.as_view(), name='user_me_oauth_token_list'),
    url(r'^(?P<pk>[0-9]+)/authorized_tokens/$', UserMeOAuth2AuthorizedTokenList.as_view(), name='user_me_oauth2_authorized_token_list'),
    url(r'^(?P<pk>[0-9]+)/personal_tokens/$', UserMeOAuth2PersonalTokenList.as_view(), name='user_me_oauth2_personal_token_list'),
    
] 

__all__ = ['urls']

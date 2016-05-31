# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from users.models import Profile


class GetUserProfile(object):
    def process_request(self, request):
        request.profile = None

        if request.user.is_authenticated():
            request.profile, _ = Profile.objects.get_or_create(user=request.user)

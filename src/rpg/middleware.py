# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rpg.models import Role


class GetUserRole:
    def process_request(self, request):
        request.role = None
        request.role_locked = False

        if request.user.is_authenticated():
            try:
                request.role = Role.objects.get(user=request.user)
                request.role_locked = request.role.is_locked

            except Role.DoesNotExist:
                pass

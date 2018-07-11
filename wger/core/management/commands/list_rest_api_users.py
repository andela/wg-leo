# -*- coding: utf-8 *-*

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License


from django.core.management.base import BaseCommand, CommandError
from wger.core.models import UserProfile


class Command(BaseCommand):
    help = 'Generates a list of users created via REST API'

    def handle(self, *args, **options):
        created_users = UserProfile.objects.exclude(created_by__isnull=True)
        if not created_users:
            raise CommandError(
                'There are currently no users created via REST API'
            )
        for user in created_users:
            self.stdout.write('Username: {} Email: {} Created by: {}'.format(
                user.user.username,
                user.user.email,
                user.created_by
            ))

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
    '''
    Allows creation of users via REST API
    '''

    help = 'Allow or disallow a user the ability to create users via REST API'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)

        parser.add_argument(
            '--allow',
            action='store_true',
            dest='allow',
            help='allow creation of users'
        )

        parser.add_argument(
            '--disallow',
            action='store_true',
            dest='disallow',
            help='disallow creation of users'
        )

    def toggle_permission(self, users, allow=False):
        '''
        Helper function to allow or disallow users from creating
        users via rest API

        :param users:
        :param allow:
        :return:
        '''

        for username in users:
            try:
                profile = UserProfile.objects.get(user__username=username)
            except UserProfile.DoesNotExist:
                raise CommandError('User {} cannot be found'.format(username))

            profile.can_create_users_via_api = allow
            profile.save()

            if allow:
                self.stdout.write(
                    self.style.SUCCESS(
                        'Successfully allowed "{}" to create users'.format(
                            username
                        )
                    )
                )
            elif not allow:
                self.stdout.write(
                    self.style.SUCCESS(
                        'Successfully disallowed "{}" from creating users'
                        .format(username)
                    )
                )

    def handle(self, *args, **options):
        if options['allow']:
            self.toggle_permission(options['username'], allow=True)
        elif options['disallow']:
            self.toggle_permission(options['username'], allow=False)

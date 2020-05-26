from django.core.management.base import BaseCommand, CommandError
import os


class Command(BaseCommand):
    help = "Renames the django project to something of your choosing"

    def add_arguments(self, parser, *args, **kwargs):
        parser.add_argument('oldProjName', type=str,
                            help="The name of the old django project.")
        parser.add_argument('newProjName', type=str,
                            help="The name of the new django project.")

    def handle(self, *args, **kwargs):
        newProjName = kwargs['newProjName']
        oldProjName = kwargs['oldProjName']

        # Rename project (Specific to django 3.0)
        # Remove asgi.py if using django < 3.0

        list_o_files_to_change = [
            f'{oldProjName}/settings/base_settings.py',
            f'{oldProjName}/wsgi.py',
            f'{oldProjName}/asgi.py',
            'manage.py',
        ]

        folder_to_rename = f"{oldProjName}"

        for thefile in list_o_files_to_change:
            with open(thefile, 'r') as file:
                filedata = file.read()

            filedata = filedata.replace(f"{oldProjName}", newProjName)

            with open(thefile, 'w') as file:
                file.write(filedata)

        try:

            os.rename(folder_to_rename, newProjName)

        except:
            raise CommandError('Folder "%s" does not exist' % folder_to_rename)

        self.stdout.write(self.style.SUCCESS(
            f"Project has been renamed to {newProjName}"))

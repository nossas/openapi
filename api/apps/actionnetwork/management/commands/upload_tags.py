# import os
import csv

from django.core.management.base import BaseCommand, CommandError, CommandParser
from apps.actionnetwork.models import ActionGroup, Tag


class Command(BaseCommand):
    help = "Carrega CVS value, label para a tabela de tags"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("csv", type=str)

        parser.add_argument("--group", type=int)

    def handle(self, *args, **kwargs):
        csv_path = kwargs["csv"]
        action_group_id = kwargs['group']

        with open(csv_path) as csv_file:
            reader = csv.DictReader(csv_file)
            result = 0

            if not action_group_id:
                for action_group in ActionGroup.objects.all():
                    result += len(Tag.objects.bulk_create([
                        Tag(**x, action_group=action_group) for x in reader
                    ]))
            else:
                action_group = ActionGroup.objects.get(pk=action_group_id)
                result = len(Tag.objects.bulk_create([
                    Tag(**x, action_group=action_group) for x in reader
                ]))

            self.stdout.write(
                self.style.SUCCESS(f'"{result}" tags carregadas')
            )

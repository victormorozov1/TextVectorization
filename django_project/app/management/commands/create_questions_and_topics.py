import csv
from django.core.management.base import BaseCommand
import pandas
from typing import Generator

from app.models import Phrase, Topic


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument('-t', '--tsv-filename', type=str)
        parser.add_argument('-x', '--xlsx-filename', type=str)
        parser.add_argument('-d', '--tsv-delimiter', type=str, default='\t')
        parser.add_argument('-q', '--tsv-quotechar', type=str, default='\n')
        parser.add_argument('-qc', '--question-column-number', type=int, default=1)
        parser.add_argument('-tc', '--topic-name-column-number', type=int, default=2)
        parser.add_argument('-ac', '--answer-column-number', type=int, default=3)

    @staticmethod
    def _iter_tsv_lines(
            tsv_filename: str,
            question_column_number: int,
            topic_name_column_number: int,
            answer_column_number: int,
            delimiter: str,
            quotechar: str,
    ) -> Generator[tuple[str, str, str], None, None]:
        with open(tsv_filename) as file:
            tsv_file = csv.reader(file, delimiter=delimiter, quotechar=quotechar)
            for line in tsv_file[1:]:
                yield line[question_column_number], line[topic_name_column_number], line[answer_column_number]

    @staticmethod
    def _iter_xlsx_lines(
            xlsx_filename: str,
            question_column_number: int,
            topic_name_column_number: int,
            answer_column_number: int,
    ) -> Generator[tuple[str, str, str], None, None]:
        data = pandas.read_excel(xlsx_filename)
        question_column_key = data.columns[question_column_number]
        topic_name_column_key = data.columns[topic_name_column_number]
        answer_column_key = data.columns[answer_column_number]

        for i in range(len(data)):
            yield data[question_column_key][i], data[topic_name_column_key][i], str(data[answer_column_key][i])

    def handle(self, *args, **options):
        self.stdout.write(f'{args=}, {options=}')
        tsv_filename = options.get('tsv_filename')

        if tsv_filename:
            iter_lines = self._iter_tsv_lines(
                tsv_filename,
                options['question_column_number'],
                options['topic_name_column_number'],
                options['answer_column_number'],
                options['tsv_delimiter'],
                options['tsv_quotechar'],
            )
        else:
            iter_lines = self._iter_xlsx_lines(
                options['xlsx_filename'],
                options['question_column_number'],
                options['topic_name_column_number'],
                options['answer_column_number'],
            )

        topics, questions = [], []

        for question, topic_name, answer in iter_lines:
            topics.append(Topic(name=topic_name, answer=answer))
            questions.append(Phrase(content=question, topic=topics[-1]))

        self.stdout.write('\n'.join(map(repr, Topic.objects.bulk_create(topics))))
        self.stdout.write('\n'.join(map(repr, Phrase.objects.bulk_create(questions))))

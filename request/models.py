import json

from django.db import models
from datetime import datetime
import json

from webspiders.models import PostgreSpider
from webspiders.models import MysqlSpider

from metadata.models import Metadata
from urllib.parse import urlparse


def init_spider(connection_string):
    con = urlparse(connection_string)

    if con.scheme == 'postgresql':
        return PostgreSpider(connection_string)
    elif con.scheme == 'mysql':
        return MysqlSpider(connection_string)
    else:
        return Exception("Cannot read scheme")


class RequestManager(models.Manager):
    def create_request(self, user, connection_string):
        request = self.model()
        request.connection_string = connection_string
        request.user = user
        request.created_at = datetime.now()

        spider = init_spider(connection_string)
        response = RequestService.get_json(spider)

        metadata = Metadata.objects.create_metadata(response)
        metadata.save()
        request.metadata = metadata

        request.save()

        return request


class Request(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    connection_string = models.CharField(db_index=True, max_length=255, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('authentication.User', on_delete=models.RESTRICT, null=True)
    metadata = models.ForeignKey('metadata.Metadata', on_delete=models.RESTRICT, null=False)

    objects = RequestManager()


class RequestService:

    @staticmethod
    def get_json(spider) -> json:
        metadata = {'tables': dict()}
        tables = spider.get_tables()
        for table in tables:
            columns_comments = spider.get_comments_from_table_filed(table)
            metadata['tables'][table] = dict()
            metadata['tables'][table]['columns'] = dict()
            for key, value in columns_comments.items():
                column_comment = json.loads(value[1]) if value[1] else {}
                metadata['tables'][table]['columns'][key] = {
                    'comment': column_comment,
                    'type': spider.get_columns_type_from_table(table, key)
                }
            table_comment = spider.get_comments_from_table(table)
            metadata['tables'][table]['table_comment'] = json.loads(table_comment) if table_comment else {}


        return {'metadata': metadata, 'database': spider.get_database_info()}

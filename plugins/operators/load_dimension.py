from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentails_id="",
                 sql="",
                 table="",
                 truncate=False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id,
        self.aws_credentails_id=aws_credentails_id,
        self.sql=sql,
        self.table=table

    def execute(self, context):
        redshift=AwsHook.PostgresHook(self.redshift_conn_id)
        if self.truncate:
            redshift.run(f"truncate table{self.table}") 
        redshift.run(f"insert into {self.table} {self.sql}")

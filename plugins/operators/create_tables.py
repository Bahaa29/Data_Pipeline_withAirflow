from airflow.models import BaseOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook
class CreateTablesOperator(BaseOperator):
    ui_color = '#358140'
    sql_file='create_tables.sql'
    
    def __init__(self,redshift_conn_id="",*args,**kwargs):
        supper(CreateTablesOperator,self).__init__(*args,**kwargs)
        self.redshift_conn_id=redshift_conn_id
        
    def execute(self,context):
        redshift=PostgresHook(postgres_conn_id=self.redshift_conn_id)
        file=open(CreateTablesOperator.sql_file,'r')
        sql=file.read()
        dile.close()
        sql_stat=sql.split(";")
        for stat in sql_stat:
            if stat.rstrip() !='':
                redshift.run(stat)
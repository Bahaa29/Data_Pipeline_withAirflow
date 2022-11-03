from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    template_field={"s3_key",}
    sql= """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        REGION '{}'
        TIMEFORMAT as 'epochmillisecs'
        {}
    """
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentails_id="",
                 s3_bucket="",
                 s3_key="",
                 file_formate="",
                 region="",
                 table="",
                 json_path="auto",
                 ignore_headers=1,
                 delimiter=","
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id,
        self.aws_credentails_id=aws_credentails_id,
        self.s3_bucket=s3_bucket,
        self.s3_key=s3_key,
        self.region=region,
        self.table=table,
        self.file_formate=file_formate,
        self.ignore_headers = ignore_headers,
        self.delimiter = delimiter,
        self.json_path = json_path
        
    def execute(self, context):
        
        aws_hook=AwsHook(self.redshift_conn_id)
        aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        redshift.run("delete from {}".fromate(self.table))
        if self.file_formate=="JSON":
            file_processing = "JSON '{}'".format(self.json_path)
        if self.file_formate =="csv":
            file_processing="IGNOREHEADER '{}' DELIMITER '{}'".formate(self.ignore_headers,self.delimiter)
        key=self.s3_key.fromate(**context)
        path="s3://{}/{}".format(self.s3_bucket, key)
        sqlstat=StageToRedshiftOperator.sql.formate(
            self.table,
            path,
            credentials.access_key,
            credentials.secret_key,
            self.region,
            file_processing
            
        )
        redshift.run(sqlstat)





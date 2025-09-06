import logging
from typing import Dict, Any, List, Optional

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Global variables
g_reserved = None

class AskDatabaseResult:
    def __init__(self, executed_sql: str, execution_result: str):
        self.executed_sql = executed_sql
        self.execution_result = execution_result

class Column:
    def __init__(self, AutoIncrement, ColumnName, ColumnType, Description, Nullable):
        self.AutoIncrement = AutoIncrement
        self.ColumnName = ColumnName
        self.ColumnType = ColumnType
        self.Description = Description
        self.Nullable = Nullable

class DatabaseDetail:
    def __init__(self, DatabaseId, DbType, InstanceAlias, InstanceId, SchemaName, State):
        self.DatabaseId = DatabaseId
        self.DbType = DbType
        self.InstanceAlias = InstanceAlias
        self.InstanceId = InstanceId
        self.SchemaName = SchemaName
        self.State = State

class DatabaseInfo:
    def __init__(self, DatabaseId, DbType, Host, Port, SchemaName):
        self.DatabaseId = DatabaseId
        self.DbType = DbType
        self.Host = Host
        self.Port = Port
        self.SchemaName = SchemaName

class ExecuteScriptResult:
    def __init__(self, RequestId: str, Results: List['ResultSet'], Success: bool):
        self.RequestId = RequestId
        self.Results = Results
        self.Success = Success

    def __str__(self):
        if self.Results:
            return self.Results[0].MarkdownTable if self.Results[0].MarkdownTable else "No Markdown Table"
        return "Execution failed" if not self.Success else "Execution succeeded"

class Index:
    def __init__(self, IndexColumns, IndexName, IndexType, Unique):
        self.IndexColumns = IndexColumns
        self.IndexName = IndexName
        self.IndexType = IndexType
        self.Unique = Unique

class InstanceDetail:
    def __init__(self, InstanceAlias, InstanceId, InstanceType, State):
        self.InstanceAlias = InstanceAlias
        self.InstanceId = InstanceId
        self.InstanceType = InstanceType
        self.State = State

class InstanceInfo:
    def __init__(self, host, instance_id, port):
        self.host = host
        self.instance_id = instance_id
        self.port = port

class MyBaseModel:
    model_config = None

class ResultSet:
    def __init__(self, ColumnNames: List[str], MarkdownTable: Optional[str], RowCount: int, Rows: List[Dict[str, Any]], Success: bool):
        self.ColumnNames = ColumnNames
        self.MarkdownTable = MarkdownTable
        self.RowCount = RowCount
        self.Rows = Rows
        self.Success = Success

class SqlResult:
    def __init__(self, sql: Optional[str]):
        self.sql = sql

class TableDetail:
    def __init__(self, ColumnList, IndexList):
        self.ColumnList = ColumnList
        self.IndexList = IndexList

class ToolRegistry:
    def __init__(self, mcp):
        self.mcp = mcp
        self.default_database_id = mcp.state.default_database_id if hasattr(mcp.state, 'default_database_id') else None

    def _register_configured_db_toolset(self):
        pass

    def _register_full_toolset(self):
        pass

    def register_tools(self):
        if self.default_database_id:
            self._register_configured_db_toolset()
        else:
            self._register_full_toolset()
        return self.mcp

def _format_as_markdown_table(column_names, rows):
    header = "| " + " | ".join(column_names) + " |"
    separator = "| " + " | ".join(["---"] * len(column_names)) + " |"
    row_lines = ["| " + " | ".join([str(row[col]) for col in column_names]) + " |" for row in rows]
    return "\n".join([header, separator] + row_lines)

def add_instance(db_user, db_password, instance_resource_id, host, port, region):
    return InstanceInfo(host, instance_resource_id, port)

def configureDtsJob(region_id, job_type, source_endpoint_region, source_endpoint_instance_type, source_endpoint_engine_name, source_endpoint_instance_id, source_endpoint_user_name, source_endpoint_password, destination_endpoint_region, destination_endpoint_instance_type, destination_endpoint_engine_name, destination_endpoint_instance_id, destination_endpoint_user_name, destination_endpoint_password, db_list):
    return {
        "region_id": region_id,
        "job_type": job_type,
        "source_endpoint": {
            "region": source_endpoint_region,
            "instance_type": source_endpoint_instance_type,
            "engine_name": source_endpoint_engine_name,
            "instance_id": source_endpoint_instance_id,
            "user_name": source_endpoint_user_name,
            "password": source_endpoint_password
        },
        "destination_endpoint": {
            "region": destination_endpoint_region,
            "instance_type": destination_endpoint_instance_type,
            "engine_name": destination_endpoint_engine_name,
            "instance_id": destination_endpoint_instance_id,
            "user_name": destination_endpoint_user_name,
            "password": destination_endpoint_password
        },
        "db_list": db_list
    }

def create_client():
    pass

def execute_script(database_id, script, logic):
    return ExecuteScriptResult("request_id", [], True)

def getDtsJob(region_id, dts_job_id):
    return {"region_id": region_id, "dts_job_id": dts_job_id}

def get_database(host, port, schema_name, sid):
    return DatabaseDetail("db_id", "db_type", "instance_alias", "instance_id", schema_name, "state")

def get_dts_client(region_id):
    pass

def get_instance(host, port, sid):
    return InstanceDetail("instance_alias", "instance_id", "instance_type", "state")

def get_meta_table_detail_info(table_guid):
    return TableDetail([], [])

async def lifespan(app):
    yield

def list_tables(database_id, search_name, page_number, page_size):
    return {"database_id": database_id, "search_name": search_name, "page_number": page_number, "page_size": page_size}

def nl2sql(database_id, question, knowledge):
    return SqlResult("SELECT * FROM table")

def run_server():
    pass

def search_database(search_key, page_number, page_size):
    return [DatabaseInfo("db_id", "db_type", "host", "port", "schema_name")]

def startDtsJob(region_id, dts_job_id):
    return {"region_id": region_id, "dts_job_id": dts_job_id}
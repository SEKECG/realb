import os
from azure.identity import DefaultAzureCredential, WorkloadIdentityCredential
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder

class ADXConfig:
    def __init__(self):
        self.cluster_url = os.getenv("ADX_CLUSTER_URL")
        self.database_name = os.getenv("ADX_DATABASE_NAME")
        self.tenant_id = os.getenv("AZURE_TENANT_ID")
        self.client_id = os.getenv("AZURE_CLIENT_ID")
        self.token_file_path = os.getenv("AZURE_FEDERATED_TOKEN_FILE")

config = ADXConfig()

def get_kusto_client():
    if config.tenant_id and config.client_id and config.token_file_path:
        credential = WorkloadIdentityCredential(
            tenant_id=config.tenant_id,
            client_id=config.client_id,
            token_file_path=config.token_file_path
        )
    else:
        credential = DefaultAzureCredential()
    
    kcsb = KustoConnectionStringBuilder.with_az_auth(config.cluster_url, credential)
    return KustoClient(kcsb)

def execute_query(query):
    client = get_kusto_client()
    response = client.execute(config.database_name, query)
    return format_query_results(response.primary_results[0])

def format_query_results(result_set):
    results = []
    for row in result_set.rows:
        results.append({col: row[col] for col in result_set.columns})
    return results

def list_tables():
    query = ".show tables"
    return execute_query(query)

def get_table_schema(table_name):
    query = f".show table {table_name} schema"
    return execute_query(query)

def get_table_details(table_name):
    query = f".show table {table_name} details"
    return execute_query(query)

def sample_table_data(table_name, sample_size):
    query = f"{table_name} | take {sample_size}"
    return execute_query(query)
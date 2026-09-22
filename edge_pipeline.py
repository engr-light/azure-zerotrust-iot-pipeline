import os
import json
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient

# Force Python to ignore the cache and read the .env file
load_dotenv(override=True)

tenant_id = os.getenv("AZURE_TENANT_ID")
client_id = os.getenv("AZURE_CLIENT_ID")
client_secret = os.getenv("AZURE_CLIENT_SECRET")
vault_url = os.getenv("KEY_VAULT_URL")

print(f"Tenant ID loaded: {tenant_id}")
print(f"Vault URL loaded: {vault_url}")  # We need to see this print!

print("[*] Authenticating edge device identity...")
# 2. Authenticate the Service Principal
credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)

print("[*] Contacting Azure Key Vault...")
# 3. Retrieve the locked Storage URL from the Key Vault
secret_client = SecretClient(vault_url=vault_url, credential=credential)
storage_secret = secret_client.get_secret("StorageAccountURL")
storage_url = storage_secret.value
print(f"[*] Successfully retrieved Storage URL from vault.")

# 4. Generate mock IoT telemetry (ESP32 power management simulation)
telemetry_payload = {
    "device_id": "esp32-main-relay",
    "sensor": "current_monitor",
    "voltage_v": 224.5,
    "current_a": 1.2,
    "timestamp": datetime.now(timezone.utc).isoformat()
}
payload_bytes = json.dumps(telemetry_payload).encode('utf-8')
blob_name = f"telemetry_{uuid.uuid4().hex[:8]}.json"

print(f"[*] Uploading payload {blob_name} to locked-down container...")
# 5. Connect to the locked-down Blob Storage and upload
blob_service_client = BlobServiceClient(account_url=storage_url, credential=credential)
blob_client = blob_service_client.get_blob_client(container="raw-telemetry", blob=blob_name)

blob_client.upload_blob(payload_bytes, overwrite=True)
print("[*] Upload complete. Zero-Trust pipeline executed successfully.")
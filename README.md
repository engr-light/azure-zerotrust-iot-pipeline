# Secure IoT Telemetry Pipeline via Azure Zero-Trust Architecture

## Executive Summary
A Python-based edge data pipeline engineered to securely route real-time smart home power metrics (voltage and current) from an ESP32 IoT prototype directly into Azure Blob Storage. Built strictly upon a Zero-Trust security model, this architecture ensures that remote edge devices never hold hardcoded infrastructure URLs or direct database connection strings, significantly reducing the attack surface for distributed hardware deployments.

## Architecture Flow
The data ingestion lifecycle operates through a heavily authenticated, four-stage zero-trust bridge:
1. **The Edge Device (Data Collection):** An ESP32 microcontroller and accompanying Python script act as the remote telemetry agent, collecting real-time power metrics and preparing the JSON payload for transmission.
2. **Microsoft Entra ID (Identity Verification):** Upon execution, the pipeline authenticates via a dedicated Service Principal. Entra ID verifies the edge device's exact Client ID and Secret, issuing a temporary cryptographic token.
3. **Azure Key Vault (Dynamic Routing):** Armed with the Entra ID token, the pipeline queries a locked-down Azure Key Vault. Authorized via explicit Data-Plane Access Policies, the vault dynamically dispenses the encrypted Storage Account URL, ensuring the edge device only learns its destination at runtime.
4. **Azure Blob Storage (Secure Ingestion):** The pipeline utilizes the dynamically retrieved URL to establish a strict TLS connection to the storage account. Governed by Azure Role-Based Access Control (RBAC), the payload is seamlessly written to the `raw-telemetry` container.

## Security Implementations
This project demonstrates a comprehensive understanding of Azure identity management, least-privilege principles, and cloud security architectures:
* **Identity-First Perimeter:** Completely eliminates hardcoded connection strings by utilizing Microsoft Entra ID Service Principals for secure machine-to-machine authentication.
* **Granular Key Vault Authorization:** Implements explicit legacy Key Vault Access Policies targeting the specific `Get` secret permission, isolating data-plane read access from broader control-plane permissions.
* **Least-Privilege RBAC:** Enforces strict Role-Based Access Control at the storage layer, granting the pipeline the exact `Storage Blob Data Contributor` role necessary for ingestion while explicitly denying overarching administrative access.
* **Cryptographic Time-Stamping:** Relies on strict UTC clock synchronization to prevent malicious replay attacks during blob transmission.
* **Environment Isolation:** Utilizes localized `.env` configurations quarantined via `.gitignore` to prevent cryptographic secret leakage in version control.

## Tech Stack
* **Language:** Python, MicroPython
* **Cloud Infrastructure:** Azure Key Vault, Azure Blob Storage, Microsoft Entra ID
* **Libraries:** Azure Identity SDK, Azure Key Vault Secrets SDK, Azure Storage Blob SDK
* **Hardware/Edge:** ESP32 Microcontroller, Relay Modules, Current/Voltage Sensors
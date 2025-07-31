# server.py
from mcp.server.fastmcp import FastMCP
import requests


mcp = FastMCP("eai-mcp-server_1", host="0.0.0.0", port= 8000)

BASIC_AUTH_USERNAME = "ID063066"
BASIC_AUTH_PASSWORD = "Svy@#4444"

# @mcp.tool()
# def fetch_url(url: str) -> dict:
#     try:
#         response = requests.get(
#             url,
#             timeout=10,
#             auth=(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD),
#             verify=False
#         )
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         return {"error": str(e)}


# New tool for POST requests to fixed endpoints
# @mcp.tool()
# def post_sync_job_management_report(report_name: str, payload: dict = None) -> dict:
#     """
#     Posts data to a SyncJobManagement endpoint.
#     report_name: User-friendly name or endpoint, e.g., 'cable report', 'segment report', or 'fetchCableReport'.
#     payload: Dictionary to send as JSON body in the POST request.
#     """
#     report_map = {
#         'cable report': 'fetchCableReport',
#         'segment report': 'fetchCableSegmentReport',
#         # Add more mappings as needed
#     }
#     endpoint = report_map.get(report_name.strip().lower(), report_name)
#     base_url = "https://eai.int.itservices.lan/oss-core-ws/rest/ressync-adv/SyncJobManagement/"
#     url = f"{base_url}{endpoint}"
#     try:
#         response = requests.post(
#             url,
#             json=payload or {},
#             timeout=10,
#             auth=(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD),
#             verify=False  # Use CA cert from certs directory for SSL verification
#         )
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         return {"error": str(e)}


# New tool for POST to CommonService/downloadRingReport
@mcp.tool()
def download_ring_report(mplsCloud: str) -> dict:
    """
    Downloads a ring report from the CommonService endpoint using the given MPLS cloud name.
    mplsCloud: The MPLS cloud name to include in the payload.
    """
    url = "https://eai.int.itservices.lan/oss-core-ws/rest/cmn-adv/CommonService/downloadRingReport"
    payload = {
        "type": "cmn-adv/commonservice/downloadringreport",
        "mplsCloud": mplsCloud
    }
    try:
        response = requests.post(
            url,
            json=payload,
            timeout=10,
            auth=(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD),
            verify=False  # Use CA cert from certs directory for SSL verification
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def fetch_sync_job_management_report(report_name: str) -> dict:
    """
    Fetches a report from SyncJobManagement.
    report_name: User-friendly name or endpoint, e.g., 'cable report', 'segment report', or 'fetchCableReport'.
    """
    # Mapping of user-friendly names to endpoints
    report_map = {
        'cable report': 'fetchCableReport',
        'segment report': 'fetchCableSegmentReport',
        # Add more mappings as needed
    }
    # Normalize input and map to endpoint
    endpoint = report_map.get(report_name.strip().lower(), report_name)
    base_url = "https://eai.int.itservices.lan/oss-core-ws/rest/ressync-adv/SyncJobManagement/"
    url = f"{base_url}{endpoint}"
    try:
        response = requests.get(
            url,
            timeout=10,
            auth=(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD),
            verify=False  # Use CA cert from certs directory for SSL verification
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # Initialize and run the MCP server
    mcp.run(transport='streamable-http')

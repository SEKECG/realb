import requests

CHROME_VERSION = "114.0.5735.110"
EDGE_VERSION = "114.0.1823.67"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36"

def download_extension(url, output_path):
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    response.raise_for_status()
    with open(output_path, "wb") as file:
        file.write(response.content)

def get_chrome_extension_url(extension_id, chrome_version):
    return f"https://clients2.google.com/service/update2/crx?response=redirect&prodversion={chrome_version}&x=id%3D{extension_id}%26installsource%3Dondemand%26uc"

def get_edge_extension_url(extension_id, edge_version):
    return f"https://edge.microsoft.com/extensionwebstorebase/v1/crx?response=redirect&prodversion={edge_version}&x=id%3D{extension_id}%26installsource%3Dondemand%26uc"
import os
import zipfile
import hashlib
import json
from typing import List, Dict, Union, Optional
from models import ChromeManifest, RiskLevel, BackgroundConfig, CrossOriginPolicy, ExternallyConnectable, FileSystemProviderCapabilities, ImportConfig, IncognitoMode, OmniboxConfig, OptionsUI, PermissionRiskMapping, RiskReport, SidePanel, Storage
from download import download_extension, get_chrome_extension_url, get_edge_extension_url

class Extension:
    def __init__(self, extension_id, browser, working_dir):
        self.extension_id = extension_id
        self.browser = browser
        self.working_dir = working_dir
        self.extension_dir_path = os.path.join(working_dir, extension_id)
        self.extension_zip_path = os.path.join(self.extension_dir_path, f"{extension_id}.zip")
        self.manifest = None
        self.name = None
        self.version = None
        self.author = None
        self.homepage_url = None
        self.permissions = []
        self.javascript_files = []
        self.urls = []
        self.sha256 = None

    def __enter__(self):
        self.__download_extension()
        self.__unzip_extension()
        self.manifest = self.__get_manifest()
        self.name = self.manifest.name
        self.version = self.manifest.version
        self.author = self.manifest.author
        self.homepage_url = self.manifest.homepage_url
        self.permissions = self.manifest.permissions
        self.javascript_files = self.__get_javascript_files()
        self.urls = self.__get_urls()
        self.sha256 = self.__calculate_sha256()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __download_extension(self):
        if self.browser == "chrome":
            url = get_chrome_extension_url(self.extension_id, "latest")
        elif self.browser == "edge":
            url = get_edge_extension_url(self.extension_id, "latest")
        else:
            raise InvalidExtensionIDError("Invalid browser specified")
        download_extension(url, self.extension_zip_path)

    def __unzip_extension(self):
        with zipfile.ZipFile(self.extension_zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.extension_dir_path)

    def __get_manifest(self):
        manifest_path = os.path.join(self.extension_dir_path, "manifest.json")
        with open(manifest_path, 'r') as file:
            manifest_data = json.load(file)
        return ChromeManifest(**manifest_data)

    def __get_javascript_files(self):
        js_files = []
        for root, _, files in os.walk(self.extension_dir_path):
            for file in files:
                if file.endswith(".js"):
                    js_files.append(os.path.join(root, file))
        return js_files

    def __get_urls(self):
        urls = []
        for js_file in self.javascript_files:
            with open(js_file, 'r') as file:
                content = file.read()
                urls.extend(self.__extract_urls(content))
        return urls

    def __extract_urls(self, content):
        # Dummy implementation for URL extraction
        return []

    def __calculate_sha256(self):
        sha256_hash = hashlib.sha256()
        with open(self.extension_zip_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    @property
    def author(self):
        return self._author

    @property
    def homepage_url(self):
        return self._homepage_url

    @property
    def javascript_files(self):
        return self._javascript_files

    @property
    def manifest_version(self):
        return self._manifest_version

    @property
    def name(self):
        return self._name

    @property
    def permissions(self):
        return self._permissions

    @property
    def urls(self):
        return self._urls

    @property
    def version(self):
        return self._version

class Browser:
    CHROME = "chrome"
    EDGE = "edge"

class InvalidExtensionIDError(Exception):
    pass
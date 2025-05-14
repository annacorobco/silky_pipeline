from abc import ABC, abstractmethod
from typing import Dict, Any

from models import UnifiedAsset, HostAssetAccount, HostAssetInterface,\
    HostAssetOpenPort, HostAssetProcessor, HostAssetSoftware, Policy, MetaInfo
from utils import safe_date


class BaseProcessing(ABC):
    def __init__(self, data: Dict[str, Any]) -> None:
        self.base_model = UnifiedAsset
        self.data = data

    @abstractmethod
    def normalize(self) -> None:
        pass


class QualysProcessing(BaseProcessing):
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.data = data

    def normalize(self) -> "self.base_model":
        for entry in self.data:
            yield self.base_model(
                _id=str(entry.get("id")),
                address=entry.get("address"),
                name=entry.get("name"),
                fqdn=entry.get("fqdn"),
                hostname=entry.get("dnsHostName"),
                created=safe_date(entry.get("created")),
                modified=safe_date(entry.get("modified")),
                last_compliance_scan=safe_date(entry.get("lastComplianceScan")),
                last_system_boot=safe_date(entry.get("lastSystemBoot")),
                last_vuln_scan=safe_date(entry.get("lastVulnScan", {}).get("$date")),
                agent_version=entry.get("agentInfo", {}).get("agentVersion"),
                platform_name=entry.get("agentInfo", {}).get("platform"),
                manufacturer=entry.get("manufacturer"),
                model=entry.get("model"),
                kernel_version=None,

                accounts=[
                    HostAssetAccount(username=a["HostAssetAccount"]["username"])
                    for a in entry.get("account", {}).get("list", [])
                ],

                network_interfaces=[
                    HostAssetInterface(**i["HostAssetInterface"])
                    for i in entry.get("networkInterface", {}).get("list", [])
                ],

                open_ports=[
                    HostAssetOpenPort(**p["HostAssetOpenPort"])
                    for p in entry.get("openPort", {}).get("list", [])
                ],

                processors=[
                    HostAssetProcessor(**cpu["HostAssetProcessor"])
                    for cpu in entry.get("processor", {}).get("list", [])
                ],

                software=[
                    HostAssetSoftware(**s["HostAssetSoftware"])
                    for s in entry.get("software", {}).get("list", [])
                ],
            )

class CrowdstrikeProcessing(BaseProcessing):
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.data = data

    def normalize(self) -> "self.base_model":
        for entry in self.data:
            policies = [
                Policy(**{**p,
                          "assigned_date": safe_date(p.get("assigned_date")),
                          "applied_date": safe_date(p.get("applied_date"))})
                for p in entry.get("policies", [])
            ]

            yield self.base_model(
                _id=entry.get("device_id"),
                device_id=entry.get("device_id"),
                instance_id=entry.get("instance_id"),
                agent_version=entry.get("agent_version"),
                platform_name=entry.get("platform_name"),
                os_version=entry.get("os_version"),
                hostname=entry.get("hostname"),
                local_ip=entry.get("local_ip"),
                external_ip=entry.get("external_ip"),
                mac_address=entry.get("mac_address"),
                connection_ip=entry.get("connection_ip"),
                default_gateway_ip=entry.get("default_gateway_ip"),
                bios_version=entry.get("bios_version"),
                bios_manufacturer=entry.get("bios_manufacturer"),
                kernel_version=entry.get("kernel_version"),
                cpu_signature=entry.get("cpu_signature"),
                service_provider=entry.get("service_provider"),
                service_provider_account_id=entry.get("service_provider_account_id"),
                system_manufacturer=entry.get("system_manufacturer"),
                system_product_name=entry.get("system_product_name"),
                first_seen=safe_date(entry.get("first_seen")),
                last_seen=safe_date(entry.get("last_seen")),
                modified=safe_date(entry.get("modified_timestamp", {}).get("$date")),
                reduced_functionality_mode=entry.get("reduced_functionality_mode"),
                provision_status=entry.get("provision_status"),
                status=entry.get("status"),
                policies=policies,
                meta_info=MetaInfo(**entry.get("meta", {})),
                tags=entry.get("tags", []),
                groups=entry.get("groups", []),
                group_hash=entry.get("group_hash"),
                product_type_desc=entry.get("product_type_desc"),
                zone_group=entry.get("zone_group"),
            )

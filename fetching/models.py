from mongoengine import (
    Document, EmbeddedDocument, StringField, IntField, FloatField,
    BooleanField, DateTimeField, ListField, EmbeddedDocumentField
)

# Unified model
class HostAssetAccount(EmbeddedDocument):
    username = StringField()

class HostAssetInterface(EmbeddedDocument):
    interfaceName = StringField()
    macAddress = StringField()
    gatewayAddress = StringField()
    address = StringField()
    hostname = StringField()

class HostAssetOpenPort(EmbeddedDocument):
    serviceName = StringField()
    protocol = StringField()
    port = IntField()

class HostAssetProcessor(EmbeddedDocument):
    name = StringField()
    speed = IntField()

class HostAssetSoftware(EmbeddedDocument):
    name = StringField()
    version = StringField()

class ActivationKey(EmbeddedDocument):
    title = StringField()
    activationId = StringField()

class ManifestVersion(EmbeddedDocument):
    sca = StringField()
    vm = StringField()

class AgentConfiguration(EmbeddedDocument):
    id = IntField()
    name = StringField()

class AgentInfo(EmbeddedDocument):
    location = StringField()
    locationGeoLatitude = FloatField()
    locationGeoLongtitude = FloatField()
    agentVersion = StringField()
    manifestVersion = EmbeddedDocumentField(ManifestVersion)
    activatedModule = StringField()
    activationKey = EmbeddedDocumentField(ActivationKey)
    agentConfiguration = EmbeddedDocumentField(AgentConfiguration)
    status = StringField()
    chirpStatus = StringField()
    connectedFrom = StringField()
    agentId = StringField()
    platform = StringField()
    lastCheckedIn = DateTimeField()

class Policy(EmbeddedDocument):
    policy_type = StringField()
    policy_id = StringField()
    applied = BooleanField()
    settings_hash = StringField()
    assigned_date = DateTimeField()
    applied_date = DateTimeField()
    uninstall_protection = StringField()
    rule_groups = ListField()

class DevicePolicies(EmbeddedDocument):
    prevention = EmbeddedDocumentField(Policy)
    sensor_update = EmbeddedDocumentField(Policy)
    global_config = EmbeddedDocumentField(Policy)
    remote_response = EmbeddedDocumentField(Policy)

class MetaInfo(EmbeddedDocument):
    version = StringField()
    version_string = StringField()


class UnifiedAsset(Document):
    meta = {
        'indexes': [
            {'fields': ['external_ip', 'hostname', 'mac_address'], 'unique': True}
        ]
    }
    # Common identifiers
    _id = StringField(primary_key=True)
    device_id = StringField()
    instance_id = StringField()
    agent_id = StringField()
    name = StringField()
    hostname = StringField()
    fqdn = StringField()

    # Network info
    address = StringField()
    mac_address = StringField()
    local_ip = StringField()
    external_ip = StringField()
    connection_ip = StringField()
    default_gateway_ip = StringField()

    # Agent and system info
    agent_version = StringField()
    platform_name = StringField()
    os_version = StringField()
    model = StringField()
    manufacturer = StringField()
    bios_version = StringField()
    bios_manufacturer = StringField()
    system_product_name = StringField()
    system_manufacturer = StringField()
    kernel_version = StringField()
    cpu_signature = StringField()

    # Time info
    created = DateTimeField()
    modified = DateTimeField()
    last_seen = DateTimeField()
    last_checked_in = DateTimeField()
    last_vuln_scan = DateTimeField()
    last_compliance_scan = DateTimeField()
    last_system_boot = DateTimeField()
    first_seen = DateTimeField()

    # Booleans and flags
    is_docker_host = BooleanField()
    reduced_functionality_mode = StringField()
    provision_status = StringField()
    status = StringField()

    # Configuration and policy
    agent_configuration = EmbeddedDocumentField(AgentConfiguration)
    device_policies = EmbeddedDocumentField(DevicePolicies)
    policies = ListField(EmbeddedDocumentField(Policy))
    meta_info = EmbeddedDocumentField(MetaInfo)

    # Additional details
    activation_key = EmbeddedDocumentField(ActivationKey)
    manifest_version = EmbeddedDocumentField(ManifestVersion)
    group_hash = StringField()
    zone_group = StringField()
    service_provider = StringField()
    service_provider_account_id = StringField()
    platform_id = StringField()
    product_type_desc = StringField()
    tags = ListField(StringField())
    groups = ListField(StringField())

    # Nested structures
    network_interfaces = ListField(EmbeddedDocumentField(HostAssetInterface))
    open_ports = ListField(EmbeddedDocumentField(HostAssetOpenPort))
    processors = ListField(EmbeddedDocumentField(HostAssetProcessor))
    software = ListField(EmbeddedDocumentField(HostAssetSoftware))
    accounts = ListField(EmbeddedDocumentField(HostAssetAccount))

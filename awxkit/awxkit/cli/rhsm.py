import random
from rhsm.connection import UEPConnection, RestlibException


def register_consumer(username, password, pool_id, quantity=None, verify=True):
    uep = UEPConnection(username=username, password=password, insecure=not verify)
    consumer = {}
    consumer['org'] = None
    consumer['name'] = "Ansible-Tower-" + str(random.randint(1, 1000000000))
    facts = {
        "system.certificate_version": "3.2",
        "tower.install_type": 'traditional',
        "uname.machine": "x86_64",
    }
    try:
        # Register consumer
        consumer_resp = uep.registerConsumer(
            name=consumer['name'],
            type="system",
            owner=consumer['org'],
            facts=facts
        )
        consumer['uuid'] = consumer_resp['uuid']
        quantity = quantity or uep.getPool(
            poolId=pool_id, consumerId=consumer['uuid']
        )['quantity']
        attach = uep.bindByEntitlementPool(
            consumerId=consumer['uuid'], poolId=pool_id, quantity=quantity
        )
        consumer['serial_id'] = str(attach[0]['certificates'][0]['serial']['id'])
    except RestlibException:
        raise

    try:
        entitlements = uep.getCertificates(
            consumer_uuid=consumer['uuid'],
            serials=[consumer['serial_id']]
        )
        for entitlement in entitlements:
            return entitlement['cert'] + entitlement['key']
    finally:
        uep.unbindByPoolId(consumer['uuid'], pool_id)

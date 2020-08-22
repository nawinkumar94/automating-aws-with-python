# -*- coding: utf-8 -*-
"""Class for Route 53 domain."""
import uuid

class DomainManager:
    """Manage an Route53 Domain."""

    def __init__(self, session):
        self.session = session
        self.route53 = self.session.client('route53')

    def find_hosted_zone(self, domain_name):
        """To find the  hosted zone for the domain name."""
        print("find_hosted_zone "+domain_name)
        paginator = self.route53.get_paginator('list_hosted_zones')
        for page in paginator.paginate():
            for zone in page['HostedZones']:
                # Domain name will contain the alias at front,
                # so we are matching the end word of Domain name with hosted zone name using '-1'
                if domain_name.endswith(zone['Name'][:-1]):
                    return zone

        return None

    def create_hosted_zone(self, domain_name):
        """Creating the hosted zone if we don't find any hosted zone."""
        print('domain_name '+domain_name)
        zone_name = '.'.join(domain_name.split('.')[-2:]) + '.'
        return self.route53.create_hosted_zone(
            Name = zone_name ,
            CallerReference = str(uuid.uuid4())
            )

    def create_s3_domain_record(self, zone, domain_name, endpoint):
        """ Creating the alias with the s3 domain."""
        self.route53.change_resource_record_sets(
            HostedZoneId = zone['id'],
            ChangeBatch={
                'Comment': "created this s3 alias from webotron",
                'Changes': [{
                        'Action':'UPSERT',
                        'ResourceRecordSet': {
                            'Name': domain_name,
                            'Type': 'A',
                            'AliasTarget': {
                                'HostedZoneId': endpoint.zone,
                                'DNSName': endpoint.host,
                                'EvaluateTargetHealth':False
                            }
                        }
                    }]
                }
            )

    def create_cf_domain_record(self, zone, domain_name, cf_domain):
        """Create a domain record in zone for domain_name."""
        return self.client.change_resource_record_sets(
            HostedZoneId=zone['Id'],
            ChangeBatch={
                'Comment': 'Created by webotron',
                'Changes': [{
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': domain_name,
                            'Type': 'A',
                            'AliasTarget': {
                                'HostedZoneId': 'Z2FDTNDATAQYW2',
                                'DNSName': cf_domain,
                                'EvaluateTargetHealth': False
                            }
                        }
                    }
                ]
            }
        )

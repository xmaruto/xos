import os
import base64
from django.db.models import F, Q
from planetstack.config import Config
from observer.openstacksyncstep import OpenStackSyncStep
from core.models.site import *
from observer.ansible import *

class SyncControllerSiteDeployments(OpenStackSyncStep):
    requested_interval=0
    provides=[SiteDeployments]

    def fetch_pending(self, deleted=False):
        pending = super(OpenStackSyncStep, self).fetch_pending(deleted)
        return pending.filter(controller__isnull=False)

    def sync_record(self, site_deployment):

	template = os_template_env.get_template('sync_controller_site_deployments.yaml')
	tenant_fields = {'endpoint':site_deployment.controller.auth_url,
		         'admin_user': site_deployment.controller.admin_user,
		         'admin_password': site_deployment.controller.admin_password,
		         'admin_tenant': site_deployment.controller.admin_tenant,
	                 'ansible_tag': '%s@%s'%(site_deployment.site.login_base,site_deployment.deployment.name), # name of ansible playbook
		         'tenant': site_deployment.site.login_base,
		         'tenant_description': site_deployment.site.name}

	rendered = template.render(tenant_fields)
	res = run_template('sync_controller_site_deployments.yaml', tenant_fields, path='controller_site_deployments')

	if (len(res)==1):
		site_deployment.tenant_id = res[0]['id']
        	site_deployment.save()
	elif (len(res)):
		raise Exception('Could not assign roles for user %s'%tenant_fields['tenant'])
	else:
		raise Exception('Could not create or update user %s'%tenant_fields['tenant'])
            
    def delete_record(self, site_deployment):
	if site_deployment.tenant_id:
            driver = self.driver.admin_driver(controller=site_deployment.controller)
            driver.delete_tenant(site_deployment.tenant_id)

	"""
        Ansible does not support tenant deletion yet

	import pdb
	pdb.set_trace()
        template = os_template_env.get_template('delete_site_deployments.yaml')
	tenant_fields = {'endpoint':site_deployment.controller.auth_url,
		         'admin_user': site_deployment.controller.admin_user,
		         'admin_password': site_deployment.controller.admin_password,
		         'admin_tenant': 'admin',
	                 'ansible_tag': 'site_deployments/%s@%s'%(site_deployment.site_deployment.site.login_base,site_deployment.site_deployment.deployment.name), # name of ansible playbook
		         'tenant': site_deployment.site_deployment.site.login_base,
		         'delete': True}

	rendered = template.render(tenant_fields)
	res = run_template('sync_site_deployments.yaml', tenant_fields)

	if (len(res)!=1):
		raise Exception('Could not assign roles for user %s'%tenant_fields['tenant'])
	"""

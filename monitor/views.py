from pyramid.view import view_config
from monitor.models.social_worker import SocialWorker
from monitor.models.website import Website
import pdb


@view_config(route_name='home', renderer='templates/index.jinja2')
def home__index(request):
    social_worker = SocialWorker()
    sites_up = []
    sites_down = []
    for site in social_worker.sites:
        obs = site.last_observation()
        if obs and (obs.status == Website.UP):
            sites_up.append(site)
        else:
            sites_down.append(site)

    return dict(sites_up=sorted(sites_up), sites_down=sorted(sites_down))

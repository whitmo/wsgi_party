from pyramid.httpexceptions import HTTPNotFound

def get_party(request):
    registry = request.registry
    if hasattr(registry, 'partyline'):
        return registry.partyline

class PartylineHelper(object):

    def __init__(self, partyline):
        self.partyline = partyline

    def connect(self, service, listener):
        self.partyline.connect(service, listener)

    def send_all(self, service, payload):
        return self.partyline.send_all(service, payload)

class PartylineInvitation(object):

    def __init__(self, request, party):
        self.request = request
        self.party = party

def party_invite(request):
    registry = request.registry
    if registry.settings.get('partyline.connected'):
        return HTTPNotFound()
    registry.settings['partyline.connected'] = True

    key = registry.settings.get('partyline_key', 'partyline')
    partyline = request.environ.get(key)
    registry.partyline = helper = PartylineHelper(partyline)
    registry.notify(PartylineInvitation(request, helper))
    return request.response

def includeme(config):
    config.add_view(party_invite, name='__invite__')


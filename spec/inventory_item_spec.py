from mamba import describe, before
from sure import expect

IRRELEVANT_ID = 'id'
IRRELEVANT_NAME = 'irrelevant name'

class InventoryItem(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

with describe(InventoryItem) as _:

    @before.each
    def create_an_item():
        _.item = InventoryItem(IRRELEVANT_ID, IRRELEVANT_NAME)

    def it_has_an_id():
        expect(_.item.id).to.be.equal(IRRELEVANT_ID)

    def it_has_a_name():
        expect(_.item.name).to.be.equal(IRRELEVANT_NAME)

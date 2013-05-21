from mamba import describe, context, before, skip
from doublex.pyDoubles import *
from sure import *

IRRELEVANT_ID = 'irrelevant id'
IRRELEVANT_CHANGE1 = 'irrelevant change 1'
IRRELEVANT_CHANGE2 = 'irrelevant change 2'
CHANGES = [IRRELEVANT_CHANGE1, IRRELEVANT_CHANGE2]

class Repository(object):
    def __init__(self, storage):
        self.storage = storage

    def save(self, aggregate):
        for change in aggregate.uncommitted_changes:
            self.storage.push(aggregate.id, change)
        aggregate.changes_committed()


with describe(Repository) as _:

    @before.each
    def create_repository():
        _.storage = spy()
        _.aggregate_class = stub()
        _.repository = Repository(_.storage)

    @before.each
    def create_aggregate():
        _.aggregate = spy()
        _.aggregate.id = IRRELEVANT_ID
        _.aggregate.uncommitted_changes = CHANGES

    with context('saving an aggregate'):
        def it_saves_all_uncommited_changes():
            _.repository.save(_.aggregate)
            assert_that_method(_.storage.push).was_called().with_args(IRRELEVANT_ID, IRRELEVANT_CHANGE1)
            assert_that_method(_.storage.push).was_called().with_args(IRRELEVANT_ID, IRRELEVANT_CHANGE2)

        def it_marks_the_changes_as_committed():
            _.repository.save(_.aggregate)
            assert_that_method(_.aggregate.changes_committed).was_called()

    with context('finding an aggregate by id'):
        def it_returns_the_aggregate():
          when(_.storage.get_aggregate_changes).with_args(IRRELEVANT_ID).then_return(CHANGES)
          when(_.aggregate_class.from_events).with_args(CHANGES).then_return(_.aggregate)
          expect(_.repository.find_by_id(IRRELEVANT_ID)).to.be.equal(_.aggregate)

        @skip
        def it_returns_none_when_no_aggregate_with_provided_id_is_found():
            pass

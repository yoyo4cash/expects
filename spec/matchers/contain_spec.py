# -*- coding: utf-8 -*

from mamba import describe, context, before

from expects import *
from expects.testing import failure


with describe('contain') as _:
    def it_should_pass_if_list_contains_item():
        expect(_.lst).to(contain('bar'))

    def it_should_pass_if_list_contains_items():
        expect(_.lst).to(contain('bar', 'baz'))

    def it_should_pass_if_iterable_of_dicts_contains_dict():
        # https://github.com/jaimegildesagredo/expects/issues/8

        expect([{'foo': 1}, 'bar']).to(contain({'foo': 1}))

    def it_should_pass_if_iterable_contains_item():
        expect(_.itr).to(contain('bar'))

    def it_should_pass_if_iterable_contains_items():
        expect(_.itr).to(contain('bar', 'baz'))

    def it_should_pass_if_string_contains_string():
        expect(_.str).to(contain('foo'))

    def it_should_pass_if_string_contains_strings():
        expect(_.str).to(contain('foo', 'string'))

    def it_should_fail_if_list_does_not_contain_item():
        with failure("to contain 'bar' and 'foo'"):
            expect(_.lst).to(contain('bar', 'foo'))

    def it_should_fail_if_iterable_does_not_contain_item():
        with failure("to contain 'bar' and 'foo'"):
            expect(_.itr).to(contain('bar', 'foo'))

    with context('#negated'):
        def it_should_pass_if_list_does_not_contain_item():
            expect(_.lst).not_to(contain('foo'))

        def it_should_pass_if_list_does_not_contain_items():
            expect(_.lst).not_to(contain('foo', 'foobar'))

        def it_should_pass_if_list_contains_one_item_and_not_the_other():
            expect(_.lst).not_to(contain('bar', 'foo'))

        def it_should_fail_if_list_contains_item():
            with failure("not to contain 'bar'"):
                expect(_.lst).not_to(contain('bar'))

        def it_should_fail_if_list_contains_items():
            with failure("not to contain 'bar' and 'baz'"):
                expect(_.lst).not_to(contain('bar', 'baz'))

    @before.each
    def fixtures():
        _.lst = ['bar', 'baz']
        _.itr = iter(_.lst)
        _.str = 'My foo string'
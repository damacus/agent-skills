import unittest
from resolve_model import RoutingError, check, resolve


class ResolverTests(unittest.TestCase):
    def inventory(self, *models):
        return {'models': [{'id': model} if isinstance(model, str) else model for model in models]}

    def test_current_runtime_resolves_new_sol(self):
        available = self.inventory('gpt-5.6-sol', 'gpt-6-sol', 'gpt-6.1-sol', 'gpt-6-astra', 'gpt-6-luna', 'gpt-9-terra')
        self.assertEqual(resolve(available, 'sol')['model'], 'gpt-6.1-sol')

    def test_exclusions_cover_explicit_inherited_and_fallback_checks(self):
        for model in ('gpt-6-sol', 'gpt-6.0-sol', 'gpt-6.0.2-sol', 'gpt-5.6-terra', 'gpt-9-terra'):
            with self.subTest(model=model), self.assertRaises(RoutingError):
                check(self.inventory(model), model)
        with self.assertRaises(RoutingError):
            resolve(self.inventory('gpt-6-sol', 'gpt-6.0-sol'), 'sol')
        with self.assertRaises(RoutingError):
            resolve(self.inventory('gpt-9-terra'), 'terra')

    def test_new_versions_need_no_policy_edit_and_sort_numerically(self):
        self.assertEqual(resolve(self.inventory('gpt-6.9-sol', 'gpt-6.10-sol'), 'sol')['model'], 'gpt-6.10-sol')
        self.assertEqual(resolve(self.inventory('gpt-6.10-sol', 'gpt-7-sol'), 'sol')['model'], 'gpt-7-sol')

    def test_no_guessed_alias_or_stale_inheritance(self):
        for model in ('sol-latest', 'gpt-sol-latest', 'gpt-6-sol-2026-10-01'):
            with self.subTest(model=model), self.assertRaises(RoutingError):
                resolve(self.inventory(model), 'sol')
        with self.assertRaises(RoutingError):
            check(self.inventory('gpt-6.1-sol', 'gpt-6.2-sol'), 'gpt-6.1-sol')

    def test_release_availability_and_old_descriptions(self):
        blocked = [{'id': 'gpt-7-sol', 'status': 'preview'},
                   {'id': 'gpt-8-sol', 'available': False},
                   {'id': 'gpt-9-sol', 'description': 'Older generation model'},
                   {'id': 'gpt-10-sol', 'description': 'Experimental release'}]
        self.assertEqual(resolve(self.inventory('gpt-6.1-sol', *blocked), 'sol')['model'], 'gpt-6.1-sol')
        with self.assertRaises(RoutingError):
            resolve(self.inventory(*blocked), 'sol')

    def test_ambiguity_blocks_instead_of_guessing(self):
        with self.assertRaises(RoutingError):
            resolve(self.inventory('gpt-6.1-sol', 'gpt-6.1.0-sol'), 'sol')
        with self.assertRaises(RoutingError):
            resolve(self.inventory({'id': 'gpt-6.1-sol', 'is_latest': True}, 'gpt-6.2-sol'), 'sol')

    def test_does_not_invent_reasoning_defaults(self):
        self.assertIsNone(resolve(self.inventory('gpt-6.1-sol'), 'sol')['default_reasoning_effort'])
        inventory = self.inventory({'id': 'gpt-6.1-sol', 'default_reasoning_effort': 'low', 'supported_reasoning_efforts': ['low', 'high']})
        self.assertEqual(resolve(inventory, 'sol')['default_reasoning_effort'], 'low')

    def test_other_families_resolve_independently(self):
        inventory = self.inventory('gpt-6-astra', 'gpt-6.1-astra', 'gpt-6-luna')
        self.assertEqual(resolve(inventory, 'astra')['model'], 'gpt-6.1-astra')
        self.assertEqual(resolve(inventory, 'luna')['model'], 'gpt-6-luna')


if __name__ == '__main__':
    unittest.main()

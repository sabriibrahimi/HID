import importlib
import io
import re
import sys
import traceback
import unittest

from django.core.management.base import BaseCommand


CATEGORIES = [
    ("Models", "app.tests.test_models", "app/models.py"),
    ("Forms", "app.tests.test_forms", "app/forms.py"),
    ("URLs", "app.tests.test_urls", "cakery_bakery/urls.py"),
    ("Signals", "app.tests.test_signals", "app/signals.py"),
    ("Admin", "app.tests.test_admin", "app/admin.py"),
    ("Views", "app.tests.test_views", "app/views.py and app/templates/"),
]

TEST_HINTS = {
    "BakerModelStructureTest.test_has_user_relation_to_auth_user": ("Baker must be linked to Django User.", "Baker.user in app/models.py"),
    "BakerModelStructureTest.test_has_required_profile_fields": ("Baker needs name, surname, contact_phone and email fields.", "Baker in app/models.py"),
    "CakeModelStructureTest.test_has_required_fields": ("Cake needs name, price, weight, description and picture fields.", "Cake in app/models.py"),
    "CakeModelStructureTest.test_has_baker_foreign_key": ("Each cake must identify its baker.", "Cake.baker in app/models.py"),
    "CakeFormTest.test_form_excludes_baker": ("The public cake form must not let users choose another baker.", "CakeForm.Meta in app/forms.py"),
    "CakeFormTest.test_form_contains_all_editable_cake_fields": ("The add form must expose all editable cake details.", "CakeForm in app/forms.py"),
    "CakeFormTest.test_widgets_have_bootstrap_form_control_class": ("Form widgets should use Bootstrap form-control styling.", "CakeForm.__init__ in app/forms.py"),
    "AdminRegistrationTest.test_baker_registered": ("Baker must be registered in Django admin.", "app/admin.py"),
    "AdminRegistrationTest.test_cake_registered": ("Cake must be registered in Django admin.", "app/admin.py"),
    "BakerPermissionTest.test_only_superuser_can_add_baker": ("Only superusers may add bakers.", "BakerAdmin.has_add_permission"),
    "BakerPermissionTest.test_only_superuser_can_change_baker": ("Only superusers may modify bakers.", "BakerAdmin.has_change_permission"),
    "BakerPermissionTest.test_only_superuser_can_delete_baker": ("Only superusers may delete bakers.", "BakerAdmin.has_delete_permission"),
    "BakerQuerysetTest.test_superuser_sees_only_bakers_with_fewer_than_five_cakes": ("Superusers must be shown bakers with fewer than five cakes.", "BakerAdmin.get_queryset"),
    "CakePermissionTest.test_owner_and_superuser_can_change_cake": ("The owning baker and superuser may modify a cake.", "CakeAdmin.has_change_permission"),
    "CakePermissionTest.test_other_baker_cannot_change_cake": ("Other bakers must not modify someone else's cake.", "CakeAdmin.has_change_permission"),
    "CakePermissionTest.test_other_baker_cannot_delete_cake": ("Other bakers must not delete someone else's cake.", "CakeAdmin.has_delete_permission"),
    "CakePermissionTest.test_other_baker_can_see_cake": ("Other bakers may still see cakes they do not own.", "CakeAdmin.get_queryset"),
    "CakePermissionTest.test_save_model_assigns_current_baker_on_create": ("A newly added cake must be assigned to the current baker.", "CakeAdmin.save_model"),
    "CakePermissionTest.test_baker_cannot_add_more_than_ten_cakes": ("A baker may have at most 10 cakes.", "CakeAdmin.has_add_permission or validation"),
    "CakePermissionTest.test_baker_cannot_exceed_total_price_10000": ("A baker's cakes may not total more than 10,000.", "Cake validation or CakeAdmin.save_model"),
    "CakePermissionTest.test_duplicate_cake_name_is_rejected": ("A cake cannot be added when its name already exists.", "Cake constraint/validation or CakeAdmin form/save_model"),
    "BakerDeletionRedistributionTest.test_deleted_bakers_cakes_are_redistributed": ("Deleting a baker must preserve and redistribute their cakes.", "pre_delete receiver in app/signals.py and Cake.baker on_delete"),
    "UrlRoutingTest.test_home_route_exists": ("The home page must have a route.", "cakery_bakery/urls.py"),
    "UrlRoutingTest.test_add_cake_route_exists": ("The add-cake page must have a named route.", "cakery_bakery/urls.py"),
    "IndexViewTest.test_home_returns_200_and_displays_all_cakes": ("The home page must display all cakes.", "index view and template"),
    "AddCakeViewTest.test_post_creates_cake_for_logged_in_baker": ("Posting the add form must create a cake owned by the logged-in baker.", "add-cake view"),
    "AddCakeViewTest.test_anonymous_user_cannot_create_cake": ("Anonymous users must not create cakes.", "login protection in add-cake view"),
}


class _C:
    GREEN = "\033[32m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    DIM = "\033[2m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def _strip(text):
    return re.sub(r"\033\[[0-9;]*m", "", text)


def _last_line(trace):
    return next((line.strip() for line in reversed(trace.strip().splitlines()) if line.strip()), "")


class Command(BaseCommand):
    help = "Run the cakery_bakery auto-grader with human-friendly output."

    def handle(self, *args, **options):
        self.use_color = not options.get("no_color", False) and sys.stdout.isatty()
        self._title("Pre-flight checks")
        if not self._preflight():
            self._line(f"{_C.RED}Cannot run tests until the project imports cleanly.{_C.RESET}")
            return
        self._title("Running tests")
        results = self._run_categories()
        passed = sum(result["passed"] for result in results)
        total = sum(result["total"] for result in results)
        self._line("")
        if passed == total:
            self._line(f"  {_C.BOLD}{_C.GREEN}ALL {total} TESTS PASS{_C.RESET}")
        else:
            self._line(f"  {_C.BOLD}{passed}/{total} tests passing ({total - passed} failing){_C.RESET}")
            self._failures(results)
            raise SystemExit(1)

    def _emit(self, text):
        self.stdout.write(text if self.use_color else _strip(text))

    def _line(self, text=""):
        self._emit(text)

    def _title(self, text):
        bar = "=" * 60
        self._line("")
        self._line(f"{_C.BOLD}{_C.CYAN}{bar}{_C.RESET}")
        self._line(f"{_C.BOLD}{_C.CYAN}  {text}{_C.RESET}")
        self._line(f"{_C.BOLD}{_C.CYAN}{bar}{_C.RESET}")

    def _preflight(self):
        ok = True
        for module in ("app.models", "app.forms", "app.admin", "app.signals", "app.views", "cakery_bakery.urls"):
            try:
                importlib.import_module(module)
                self._line(f"  {_C.GREEN}OK{_C.RESET}   {module}")
            except Exception as exc:
                ok = False
                self._line(f"  {_C.RED}FAIL{_C.RESET} {module}: {exc}")
        try:
            from django.core.management import call_command
            call_command("makemigrations", "app", check=True, dry_run=True, verbosity=0)
            self._line(f"  {_C.GREEN}OK{_C.RESET}   models match migrations")
        except SystemExit:
            self._line(f"  {_C.YELLOW}WARN{_C.RESET} app models have changes not captured in a migration")
        except Exception as exc:
            self._line(f"  {_C.YELLOW}WARN{_C.RESET} could not verify migrations: {exc}")
        return ok

    def _run_categories(self):
        from django.test.runner import DiscoverRunner
        runner = DiscoverRunner(verbosity=0, interactive=False)
        runner.setup_test_environment()
        old_config = runner.setup_databases()
        try:
            return [
                self._run_one(index, label, dotted, fallback)
                for index, (label, dotted, fallback) in enumerate(CATEGORIES, 1)
            ]
        finally:
            runner.teardown_databases(old_config)
            runner.teardown_test_environment()

    def _run_one(self, index, label, dotted, fallback):
        result = unittest.TestResult()
        suite = unittest.defaultTestLoader.loadTestsFromName(dotted)
        buffer = io.StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        sys.stdout = sys.stderr = buffer
        try:
            suite.run(result)
        finally:
            sys.stdout, sys.stderr = old_out, old_err
        bad = result.failures + result.errors
        passed = result.testsRun - len(bad)
        status = f"{_C.GREEN}OK{_C.RESET}" if not bad else f"{_C.RED}FAIL{_C.RESET}"
        self._line(f"  [{index}/{len(CATEGORIES)}] {label:<10} {self._bar(passed, result.testsRun)} {status} {passed}/{result.testsRun}")
        failures = []
        for test, trace in bad:
            test_id = test.id() if hasattr(test, "id") else str(test)
            short = ".".join(test_id.split(".")[-2:])
            requirement, where = TEST_HINTS.get(short, (short, fallback))
            failures.append({"test_id": test_id, "requirement": requirement, "where": where, "error": _last_line(trace)})
        return {"label": label, "total": result.testsRun, "passed": passed, "failures": failures}

    def _bar(self, passed, total, width=24):
        filled = int(round(width * passed / total)) if total else 0
        return f"{_C.GREEN}{'#' * filled}{_C.RESET}{_C.DIM}{'.' * (width - filled)}{_C.RESET}"

    def _failures(self, results):
        self._title("Failures - what to fix")
        for result in results:
            for failure in result["failures"]:
                self._line("")
                self._line(f"  {_C.RED}FAIL{_C.RESET} {_C.BOLD}{result['label']}{_C.RESET} -> {failure['test_id'].split('.')[-1]}")
                self._line(f"        {_C.BOLD}Requirement:{_C.RESET} {failure['requirement']}")
                self._line(f"        {_C.BOLD}Where:{_C.RESET}       {failure['where']}")
                self._line(f"        {_C.BOLD}Error:{_C.RESET}       {_C.DIM}{failure['error']}{_C.RESET}")

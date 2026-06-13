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
    ("URLs", "app.tests.test_urls", "real_estate/urls.py"),
    ("Signals", "app.tests.test_signals", "app/signals.py"),
    ("Admin", "app.tests.test_admin", "app/admin.py"),
    ("Views", "app.tests.test_views", "app/views.py and app/templates/"),
]


TEST_HINTS = {
    "PropertyModelStructureTest.test_has_required_fields": ("Property must expose name, description, area, date, image, reserved and sold fields.", "Property in app/models.py"),
    "PropertyModelStructureTest.test_feature_summary_field_exists_for_edit_display": ("Property must keep/display a comma-separated feature summary.", "Property.feature in app/models.py or the edit.html view/template"),
    "AgentModelStructureTest.test_has_required_profile_fields": ("Agent must expose name, surname, phone, LinkedIn, completed sales and email.", "Agent in app/models.py"),
    "AgentModelStructureTest.test_has_user_one_to_one_to_auth_user": ("Agent must be linked to Django User.", "Agent.user in app/models.py"),
    "FeatureModelStructureTest.test_has_name_and_value_fields": ("Feature must have a name and a numeric value used for pricing.", "Feature in app/models.py"),
    "ThroughModelStructureTest.test_property_agent_links_property_and_agent": ("Property-agent responsibility must be represented with a through model.", "PropertyAgent in app/models.py"),
    "ThroughModelStructureTest.test_property_feature_links_property_and_feature": ("Property-feature assignment must be represented with a through model.", "PropertyFeature in app/models.py"),
    "EditFormTest.test_feature_summary_is_not_user_editable": ("Features can be displayed on edit.html, but cannot be added or removed through the form.", "EditForm in app/forms.py"),
    "AdminRegistrationTest.test_models_are_registered": ("Agent, Feature and Property must be registered in Django admin.", "app/admin.py"),
    "AgentAndFeaturePermissionTest.test_only_superusers_can_add_agents": ("Only superusers can add agents.", "AgentAdmin.has_add_permission"),
    "AgentAndFeaturePermissionTest.test_only_superusers_can_add_features": ("Only superusers can add features.", "FeatureAdmin.has_add_permission"),
    "PropertyAdminPermissionTest.test_only_agents_can_add_property_listings": ("Only agents can add property sale listings.", "PropertyAdmin.has_add_permission"),
    "PropertyAdminPermissionTest.test_save_model_assigns_current_agent_on_create": ("The creating agent must be assigned to the new property.", "PropertyAdmin.save_model"),
    "PropertyAdminPermissionTest.test_responsible_agent_can_change_listing": ("Responsible agents can modify their listings.", "PropertyAdmin.has_change_permission"),
    "PropertyAdminPermissionTest.test_other_agent_can_view_but_not_change_listing": ("Other agents may view listings but must not change them.", "PropertyAdmin.has_change_permission/get_queryset"),
    "PropertyAdminPermissionTest.test_listing_can_only_be_deleted_without_features": ("Listings can be deleted only when no features are attached.", "PropertyAdmin.has_delete_permission"),
    "PropertyAdminPermissionTest.test_superuser_sees_only_today_listings": ("Superusers in admin see only listings published today.", "PropertyAdmin.get_queryset"),
    "PropertySoldSignalTest.test_marking_property_sold_increments_all_assigned_agents": ("When a property is marked sold, every assigned agent's completed sales count increments.", "app/signals.py"),
    "PropertySoldSignalTest.test_saving_already_sold_property_does_not_increment_again": ("Sales counts should increment only on the transition to sold.", "app/signals.py"),
    "PropertyFeatureSignalTest.test_property_feature_summary_updates_after_feature_changes": ("Feature changes must update the comma-separated property feature display.", "app/signals.py"),
    "IndexViewTest.test_index_displays_only_unsold_properties_larger_than_100_square_meters": ("The homepage shows only unsold properties with area greater than 100 m2.", "views.index"),
    "IndexViewTest.test_index_displays_feature_based_price": ("Displayed price must be the sum of feature values.", "views.index/template"),
    "EditViewTest.test_edit_page_displays_comma_separated_features_and_price": ("The edit.html page displays comma-separated features and the calculated price.", "views.edit.html/template"),
    "EditViewTest.test_post_updates_property_information": ("The edit.html page must update editable property information.", "views.edit.html/EditForm"),
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
    help = "Run the real_estate auto-grader with human-friendly output."
    requires_system_checks = []

    def handle(self, *args, **options):
        self.use_color = not options.get("no_color", False) and sys.stdout.isatty()
        self._title("Pre-flight checks")
        if not self._preflight():
            self._line(f"{_C.RED}Cannot run tests until the project imports cleanly.{_C.RESET}")
            raise SystemExit(1)
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
        for module in ("app.models", "app.forms", "app.admin", "app.signals", "app.views", "real_estate.urls"):
            try:
                importlib.import_module(module)
                self._line(f"  {_C.GREEN}OK{_C.RESET}   {module}")
            except Exception as exc:
                ok = False
                self._line(f"  {_C.RED}FAIL{_C.RESET} {module}: {exc}")
                for line in traceback.format_exception_only(type(exc), exc):
                    self._line(f"       {_C.DIM}{line.rstrip()}{_C.RESET}")
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
        try:
            suite = unittest.defaultTestLoader.loadTestsFromName(dotted)
        except Exception:
            trace = traceback.format_exc()
            self._line(f"  [{index}/{len(CATEGORIES)}] {label:<10} {_C.RED}IMPORT ERROR{_C.RESET}")
            return {
                "label": label,
                "total": 1,
                "passed": 0,
                "failures": [{"test_id": dotted, "requirement": f"{label} tests must import cleanly", "where": fallback, "error": _last_line(trace)}],
            }
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

import argparse
import os

from django.core.management import execute_from_command_line

# if __name__ == "__main__":
#     os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
#     django.setup()
#     TestRunner = get_runner(settings)
#     test_runner = TestRunner()
#     failures = test_runner.run_tests(["tests"])
#     sys.exit(bool(failures))


def parse_args():
    parser = argparse.ArgumentParser()
    return parser.parse_known_args()


def runtests():
    os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

    try:
        execute_from_command_line()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    runtests()

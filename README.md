#BACI Administration Apps

Small applications for administration. This will include a mileage, sick forms and new hire apps.

## Installation

1. `pip install -r -requirements.txt`
2. Tweak local settings in `/admin_apps/config/settings/local`
3. Set Environment Var to run config.settings.local `export DJANGO_SETTINGS_MODULE="config.settings.local"`
4. Make the tables `manage.py migrate`
5. Add the test data `manage.py loaddoata data.json`

## Directory

repository_root/
	django_project_root/
		configuration_root/

https://managelogs.herokuapp.com/ (live_demo)
user: demo
pass: demo1234

# LOG

Log Register


## How to development?

1. clone the repository.
2. make a virtualenv with python 3.
3. Activate virtualenv.
4. Install deps.
5. Configure an instance .env
6. Execute test.

```console
git clone git@github.com:lffsantos/demo_django_rest_framework.git demo_django_rest_framework
cd demo_django_rest_framework
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
```

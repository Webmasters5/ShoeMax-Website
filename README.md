# ShoeMax-Website
A footwear shopping website built on Django.

## Load sample data

From the project root, run:

```bash
python manage.py loaddata fixtures/sample_data.json
```

If you want to start with a clean database before loading sample data:

```bash
python manage.py flush
python manage.py loaddata fixtures/sample_data.json
```

> `flush` removes all data and resets database sequences

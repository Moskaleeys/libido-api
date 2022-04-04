export DATABASE_ENGINE=django.db.backends.mysql \
    DATABASE_HOST=libido-backend-test.cubzbc1hlyxy.ap-northeast-2.rds.amazonaws.com \
    DATABASE_PORT=3306 \
    DATABASE_NAME=libido-v2 \
    DATABASE_USER=root \
    DATABASE_PASSWORD=MoskaStudio~!1 \
    DJANGO_SECRET_KEY='django-insecure-pr*ox7h!2j8ql1*@)kt34a8ddalhlvq-bqw73ak@56gieyyj0&' \
    DJANGO_SETTINGS_MODULE=libido_api.settings.development \
    SECRET_KEY='django-insecure-pr*ox7h!2j8ql1*@)kt34a8ddalhlvq-bqw73ak@56gieyyj0&' \
    ALGORITHM=HS256 \
    YOUTUBE_DATA_API_KEY=AIzaSyCfB5jU3PMNvm-SRdNrFWiMhFgjdYBAfn8 \
    EMAIL_HOST=smtp.gmail.com \
    EMAIL_PORT=587 \
    EMAIL_HOST_USER='test.moska.bc@gmail.com' \
    EMAIL_HOST_PASSWORD='##ahtmzk999' \
    AWS_IAM_ACCESS_KEY='AKIATWD4P5YETFG735QQ' \
    AWS_IAM_SECRET_KEY='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' \
    AWS_S3_REGION_NAME=ap-northeast-2 \
    AWS_STORAGE_BUCKET_NAME=libido-dev


# export DATABASE_ENGINE=django.db.backends.mysql \
#     DATABASE_HOST=libido-prd.cubzbc1hlyxy.ap-northeast-2.rds.amazonaws.com \
#     DATABASE_PORT=3306 \
#     DATABASE_NAME=libido-prd \
#     DATABASE_USER=root \
#     DATABASE_PASSWORD=asdasdasd0 \
#     DJANGO_SECRET_KEY='django-insecure-pr*ox7h!2j8ql1*@)kt34a8ddalhlvq-bqw73ak@56gieyyj0&' \
#     DJANGO_SETTINGS_MODULE=libido_api.settings.product \
#     SECRET_KEY='django-insecure-pr*ox7h!2j8ql1*@)kt34a8ddalhlvq-bqw73ak@56gieyyj0&' \
#     YOUTUBE_DATA_API_KEY=AIzaSyCfB5jU3PMNvm-SRdNrFWiMhFgjdYBAfn8 \
#     EMAIL_HOST=smtp.gmail.com \
#     EMAIL_PORT=587 \
#     EMAIL_HOST_USER='test.moska.bc@gmail.com' \
#     EMAIL_HOST_PASSWORD='##ahtmzk999' \
#     AWS_IAM_ACCESS_KEY='AKIATWD4P5YETFG735QQ' \
#     AWS_IAM_SECRET_KEY='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' \
#     AWS_S3_REGION_NAME=ap-northeast-2 \
#     AWS_STORAGE_BUCKET_NAME=libido-prd-api 




# for development


cd libido_api && python3 manage.py runserver 8888 --settings=libido_api.settings.development

# cd libido_api && daphne -b 0.0.0.0 -p 8000 --proxy-headers libido_api.asgi:application

# cd libido_api && python3 manage.py createsuperuser --settings=libido_api.settings.development

# cd libido_api && python3 manage.py createsuperuser --settings=libido_api.settings.product

# cd libido_api && python3 manage.py runserver --settings=libido_api.settings.product

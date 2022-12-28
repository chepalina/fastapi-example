# Python FastAPI Template


## CLI
### Запуск приложения
```sh
$ ./manage.py start api
```

### Создание миграции
```sh
$ ./manage.py migrations make my_little_migration
```

### Применение миграции
Мигрировать до актуального состояния
```sh
$ ./manage.py migrations up
```

Мигрировать до заданной миграции в сторону обновления
```sh
$ ./manage.py migrations up my_little_migration
```

Откатиться до предыдущей миграции
```sh
$ ./manage.py migrations down
```

Откатиться до заданной миграции
```sh
$ ./manage.py migrations down my_little_migration
```

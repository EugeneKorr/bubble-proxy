## 🗂️ Структура проекта

```
bubble-proxy/
├── docker-compose.yml       # Оркестрация контейнеров
├── deploy.sh               # Скрипт управления
├── .env.example            # Пример конфигурации
├── README.md               # Документация
├── nginx/
│   ├── nginx.conf          # Базовая конфигурация Nginx
│   └── conf.d/
│       └── default.conf.template  # Шаблон прокси конфига
├── monitor/
│   ├── Dockerfile          # Docker образ монитора
│   ├── check.py            # Python скрипт мониторинга
│   └── requirements.txt    # Зависимости Python
├── certbot/                # SSL сертификаты (не в git)
│   ├── conf/
│   └── www/
└── logs/                   # Логи (не в git)
    ├── nginx/
    ├── certbot/
    └── monitor/
```



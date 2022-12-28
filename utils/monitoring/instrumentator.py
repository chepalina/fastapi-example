from prometheus_fastapi_instrumentator import Instrumentator, metrics

LATENCY_BUCKETS = (0.001, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1)


def get_instrumentator(namespace: str, access_ignored_paths: list[str]) -> "Instrumentator":
    """Получить инструментатор метрик.

    :param namespace: имя приложения;
    :param access_ignored_paths: игнорируемые пути;
    :return: экземпляр инструментатора, с добавленными метриками.
    """
    instrumentator = Instrumentator(excluded_handlers=access_ignored_paths)

    instrumentator.add(
        metrics.requests(
            metric_name="http_requests_total_by_statuses",
            metric_namespace=namespace,
            should_include_method=False,
            should_include_handler=False,
        )
    )
    instrumentator.add(
        metrics.requests(
            metric_namespace=namespace,
            should_include_method=False,
            should_include_handler=False,
            should_include_status=False,
        )
    )
    instrumentator.add(
        metrics.latency(
            metric_namespace=namespace,
            should_include_method=False,
            should_include_handler=False,
            should_include_status=False,
            buckets=LATENCY_BUCKETS,
        )
    )
    return instrumentator

from django.core.cache import caches


def increment_and_get_sequence():
    """
    从Redis中获取并递增流水号
    :return: 新的流水号
    """
    cache = caches['order_serial_number']
    with cache.lock('sequence_lock'):
        global_sequence = cache.get_or_set('global_sequence', 0)
        global_sequence = (global_sequence + 1) % 1000000
        cache.set('global_sequence', global_sequence)
        return global_sequence

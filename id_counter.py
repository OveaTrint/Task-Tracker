def get_next_id(counter_file='counter.txt'):
    try:
        with open(counter_file, 'r') as f:
            current_id = int(f.read().strip())
    except FileNotFoundError:
        current_id = 0

    next_id = current_id + 1

    with open(counter_file, 'w') as f:
        f.write(str(next_id))

    return next_id
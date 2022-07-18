import sys


def str_1kb():
    return "abcde" * 195


def example_program(count_objects, object_size_kb):
    obj_list = []
    for i in range(count_objects):
        obj_list.append(
            {'key_' + str(j) : str_1kb() for j in range(object_size_kb)})
    return obj_list


if __name__ == "__main__":
    try:
        passed_args = [int(arg) for arg in sys.argv[1:3]]
    except ValueError as e:
        print(e)
        raise ValueError('Must pass integers only to use_x_amount_of_mem function.')

    result = example_program(*passed_args)
    result_size = sys.getsizeof(result)
    print(result_size)

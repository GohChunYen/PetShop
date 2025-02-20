# Python Exercise
def filter_odd_num(numbers: list):
    odd_numbers = []
    for num in numbers:
        if num % 2 != 0:
            odd_numbers.append(num)
            
    return odd_numbers

def new_filter_odd_num(numbers: list):
    return [num for num in numbers if num % 2 != 0]

def test():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(filter_odd_num(numbers))
    print(new_filter_odd_num(numbers))
    
test()

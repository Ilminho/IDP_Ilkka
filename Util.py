def roundList(list:list):
    return [int(number) for number in list]

def averageOfList(list:list):
    return sum(list)/(len(list))

def chunkSizeReducer(chunkSize, targetSize):
    print('lol')
    
    
def split_into_equal_lists(input_list, num_sublists):
    if num_sublists <= 0:
        raise ValueError("Number of sublists must be greater than zero.")
    sublist_size = len(input_list) // num_sublists
    remainder = len(input_list) % num_sublists
    sublists = []

    start = 0
    for i in range(num_sublists):
        end = start + sublist_size + (1 if i < remainder else 0)
        sublists.append(input_list[start:end])
        start = end

    return sublists


def wavelet_denoise(signal, wavelet='db4', level=5):
    """
    Apply wavelet denoising to a signal.

    Args:
        signal (numpy array): The input signal.
        wavelet (str): The wavelet function to use (default is 'db4').
        level (int): The level of decomposition (increase for more aggressive denoising).

    Returns:
        numpy array: The denoised signal.
    """
    # Decompose the signal into wavelet coefficients
    coeffs = pywt.wavedec(signal, wavelet, level=level)

    # Set threshold for coefficients
    threshold = np.median(np.abs(coeffs[-level])) / 0.6745

    # Apply soft thresholding to the coefficients
    denoised_coeffs = [pywt.threshold(c, threshold, mode='soft') for c in coeffs]

    # Reconstruct the denoised signal from the coefficients
    denoised_signal = pywt.waverec(denoised_coeffs, wavelet)

    return denoised_signal

def update_plot(frame):

    
    try:
        TIMER.setTime(CHUNK/FREQ)

        row = next(csv_stream)
        chunkToAdd=row['adc2']


        
        adc2.extend(wavelet_denoise(row['adc2']))

        if(len(adc2)>TF*FREQ):
            copy=adc2.copy()[CHUNK:]
            adc2.clear()
            adc2.extend(copy)




        ax1.clear()
        ax1.set_ylabel('Value')
        ax1.plot(adc2, label='Time passed: '+TIMER.getTime().__str__())
        ax1.set_xticks([])
        ax1.set_ylim(bottom=0, top=1000)
        ax1.legend()
    except StopIteration:
        ani.event_source.stop()

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

my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Replace with your own list
result = split_into_equal_lists(my_list, 2)

for i, sublist in enumerate(result):
    print(averageOfList(sublist))

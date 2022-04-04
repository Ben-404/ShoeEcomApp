
# Bubble sort algorithm
def sort(sorttype, products):

    # Sort low-high
    if sorttype == 'low':
        lst = len(products) 
        for i in range(0, lst): 
            
            for j in range(0, lst-i-1): 
                if (products[j][3] > products[j + 1][3]): 
                    temp = products[j] 
                    products[j]= products[j + 1] 
                    products[j + 1]= temp 
        return products

    # Sort high-low
    else:
        lst = len(products) 
        for i in range(0, lst): 
            
            for j in range(0, lst-i-1): 
                if (products[j][3] < products[j + 1][3]): 
                    temp = products[j] 
                    products[j]= products[j + 1] 
                    products[j + 1]= temp 
        return products


# =================================================
# Search algorithm


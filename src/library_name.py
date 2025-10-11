# 1. Find_largest_transaction 
# will sort transactions in order from largest to smallest by amount spent 
def sort_largest_transaction(accounts):
    unsorted_list = accounts.copy()
    sorted_list = []
    # sort until unsorted is done 
    while unsorted_list:
        largest_transaction = unsorted_list[0]
        largest_amount = largest_transaction["Amount"]

        # find transaction with largest amount
        for transaction in unsorted_list:
            if transaction["Amount"] > largest_amount:
                largest_amount = transaction["Amount"]
                largest_transaction = transaction 

        # add the largest transaction to the sorted list
        sorted_list.append(largest_transaction)

        # remove largest transaction from the unsorted list
        unsorted_list.remove(largest_transaction)

    return(sorted_list)

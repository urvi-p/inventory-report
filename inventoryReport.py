# Create daily report from inventory information
# References: Python 3 Documentation
# Author: Urvi Patel

def main():
    '''
    This function calls the other functions
    Inputs: None
    Returns: None
    '''
    list_of_items_to_order = check_items_in_stock(read_onshelves())
    items_ordering = cheapest_price(list_of_items_to_order, read_availability())
    get_product_name(items_ordering, read_products())
    total = sum(get_all_costs(items_ordering)) 
    supplier_cost_dict = total_cost_of_suppliers(items_ordering)
    highest_cost = max(supplier_cost_dict.values())
    top_suppliers_list = get_highest_cost_supplier(highest_cost, items_ordering, supplier_cost_dict)
    contents_and_file(items_ordering, highest_cost, total, top_suppliers_list)    
    print_order()   

def read_onshelves(): 
    '''
    This function reads onshelves.txt and creates a dictionary with each line.
    Inputs: None
    Returns: Dictionary of items in stock
    '''
    onshelves = open("onshelves.txt","r")
    stocked_items = {}
    for line in onshelves:
        (product_code, quantity_remaining) = line.strip().split("#")
        stocked_items[product_code] = int(quantity_remaining)
    onshelves.close()
    return stocked_items

def read_availability(): 
    '''
    This function reads availability.txt and creates a dictionary with each line.
    Inputs: None
    Returns: Dictionary of items suppliers have 
    '''
    available_items = open("availability.txt","r")
    items_available = {}
    # append all lines to a list 
    line_list = []
    for line in available_items:
        line = line.strip().split(",")
        line[2] = float(line[2])
        line_list.append(line)
    line_list = sorted(line_list, key=lambda key:key[2], reverse=True)  # sort in decending order by price    
    for line in line_list:
        (product_code,supplier_info) = line[0],[line[1],line[2]]
        items_available[product_code] = supplier_info
    available_items.close()
    return items_available

def read_products(): 
    '''
    This function reads products.txt and creates a dictionary with each line.
    Inputs: None
    Returns: Dictionary of products sold in the store
    '''
    products = open("products.txt","r")
    products_list = {}
    for line in products:
        (product_code, product_name) = line.strip().split(";")
        products_list[product_code] = product_name
    products.close()
    return products_list

def read_suppliers(): 
    '''
    This function reads suppliers.txt and creates a dictionary with each line.
    Inputs: None
    Returns: Dictionary of supplier information
    '''
    suppliers = open("suppliers.txt","r")
    supplier_info = {}
    for line in suppliers:
        line = line.strip().split(";")
        (phone_number, supplier_name) = line[0],line[1]
        supplier_info[phone_number] = supplier_name
    suppliers.close()
    return supplier_info

def check_items_in_stock(items_in_stock):
    '''
    This function checks how many items are in stock and what needs to be ordered.
    Inputs: Dictionary of items in stock
    Returns: List of items to order
    '''
    items_to_order =[] # list to contain lists for each product order
    items_list = items_in_stock.items()
    items=[]
    for item in items_list:
        if item[1] < 20:
            quantity_needed = 50 - item[1]
            items = [item[0],quantity_needed]
            items_to_order.append(items)
    return items_to_order

def cheapest_price(items_to_order, available_items): 
    '''
    This function gets the cheapest price for each product.
    Inputs: List of items to order, dictionary of available items
    Returns: Modified list of items to order
    '''    
    for item in items_to_order:
        product_code = item[0]
        price = available_items[product_code][1]
        phone_number = available_items[product_code][0]
        cost_for_item = price * item[1]
        formatted_cost = "{:7.2f}".format(cost_for_item)
        item.append(phone_number)
        item.append(float(formatted_cost))
    # items_to_order list now contains [product code, quantity needed, suppliers 
    # phone number, cost for items] for each item
    items_to_order = sorted(items_to_order, key=lambda key:key[2]) # sort by phone number
    return items_to_order

def get_product_name(items_to_order, products_list): 
    '''
    This funtion looks and the product code, gets the corresponding product name 
    and appends it to each item in the list.
    Inputs: List of items to order, dictionary of products sold in the store
    Returns: None
    '''
    for item in items_to_order:
        product_code = item[0]
        product_name = products_list[product_code]
        item.append(product_name)
    return
    
def get_all_costs(items_to_order):  
    '''
    This function creates a list of the costs of all the items.
    Inputs: List of items to order
    Returns: List containing all costs
    '''
    total_costs = []
    for item in items_to_order:
        cost = item[3]
        total_costs.append(cost)
    return total_costs

def total_cost_of_suppliers(items_to_order): 
    '''
    This function gets all the unique suppliers and creates a dictionary 
    for the cumulative cost of a supplier.
    Inputs: list of item to order
    Returns: dictionary of total cost for each supplier
    '''
    # add all values to a set so they only appear once then append to a list
    supplier_list = []
    nonrepeating_suppliers = set()
    for item in items_to_order:
        if not item[2] in nonrepeating_suppliers:
            supplier_list.append([item[2],0])
            nonrepeating_suppliers.add(item[2])
    # get dictionary of cumulative cost for each supplier
    cumulative_costs = dict(supplier_list)
    for item in items_to_order:
        if item[2] in cumulative_costs.keys():   
            cost = cumulative_costs[item[2]]+item[3]
            (supplier, total_cost) = item[2],cost
            cumulative_costs[supplier] = total_cost   
    return cumulative_costs

def get_highest_cost_supplier(highest_cost, items_to_order, supplier_cost_dict): 
    '''
    This function looks at the costs and gets the supplier(s) with the highest cost(s).
    Inputs: float(highest_cost), list of items to order, dictionary of supplier costs
    Returns: list of highest cost suppliers
    '''    
    highest_cost_suppliers=[]
    supplier_cost_list = supplier_cost_dict.items()
    for supplier in supplier_cost_list:
        if supplier[1]==highest_cost:
            highest_cost_suppliers.append(supplier[0])
    return highest_cost_suppliers

def highest_cost_supplier_info(highest_cost, items_to_order, supplier_info, top_suppliers_list): 
    '''
    This function gets the name of the highest cost supplier(s) and 
    creates a list with the information(name, phone, cost) of the supplier(s).
    Inputs: float(highest_cost), list of items to order, dictionary of supplier 
            info, list of highest cost suppliers
    Returns: List containing information about supplier(s) with highest cost 
    '''    
    # uses list of top suppliers to get the corresponding supplier information 
    highest_supplier_info =[]
    for phone_number in top_suppliers_list:
        supplier_name = supplier_info[phone_number]
        info = [supplier_name, phone_number, highest_cost]
        highest_supplier_info.append(info)
    # creates a formatted string for highest cost   
    highest_cost_lines = []
    for supplier in highest_supplier_info:
        formatted_number = "("+supplier[1][:3]+") "+supplier[1][3:-4]+" "+supplier[1][6:]
        highest = ("Highest cost: {:s} {:s} [${:.2f}]" 
                   .format(supplier[0],formatted_number,supplier[2]))
        highest_cost_lines.append(highest)    
    return highest_cost_lines
    

def format_file_lines(items_to_order): 
    '''
    This function uses string formatting and creates the different lines of the 
    order information.
    Inputs: List of items to order
    Returns: List of all the lines in the order
    '''
    lines_of_order = []
    for item in items_to_order:
        if item[1]>40:
            product_name = "*{:^17s}"
        else:
            product_name = "{:^18s}"
        formatted_number = "("+item[2][:3]+") "+item[2][3:-4]+" "+item[2][6:]
        formatted_line = (("|{:^14s}|"+product_name+"|{:7d} |{:^16s}| ${:7.2f} |")
                          .format(item[0], item[4][:16], item[1], formatted_number, item[3]))
        lines_of_order.append(formatted_line)
    return lines_of_order
    
def contents_and_file(items_to_order, highest_cost, total, top_suppliers_list): 
    '''
    This function contains the other information needed to create the daily report 
    of what needs to be ordered.
    It also calls create_file() to create the file "orders.txt".
    Inputs: List of items to order, float(highest cost), float(total cost)
    Returns: None
    '''
    divider ="+--------------+------------------+--------+----------------+----------+\n"
    header = "| Product code | Product Name     |Quantity| Supplier       | Cost     |\n" 
    order_lines = format_file_lines(items_to_order)
    total_line = ("| Total Cost   |                ${:10.2f}|\n".format(total))
    end_divider = "+--------------+---------------------------+\n"  
    highest_supplier_lines = highest_cost_supplier_info(highest_cost, items_to_order,
                                                        read_suppliers(), top_suppliers_list)
    create_file(divider, header, order_lines, total_line, end_divider, highest_supplier_lines)
    return
       
def create_file(divider, header, order_lines, total_line, end_divider, highest_supplier_lines): 
    '''
    This file creates the file containing the table of order information.
    Inputs: str(divider), str(header), list of the order lines, 
            str(total line), str(end divider), list of highest supplier info
    Returns: None
    '''
    file = open("orders.txt","w+")
    file.write("{:s}{:s}{:s}".format(divider, header, divider))
    for line in order_lines:
        file.write(line+"\n")
    file.write("{:s}{:s}{:s}".format(divider, total_line, end_divider))
    for line in highest_supplier_lines:
        file.write(line+"\n")      
    file.close()
    return
              
def print_order(): 
    '''
    This file prints the contents of the file "orders.txt".
    Inputs: None
    Returns: None
    '''
    file = open("orders.txt","r")
    print(file.read()) 
    file.close()

main()
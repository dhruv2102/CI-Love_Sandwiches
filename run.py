import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    '''
    Get sales figures
    :return:
    '''
    print("Please enter sales data from the last market.")
    print("Data should be six numbers, separated by commas.")
    print("Example: 10,20,30,40,50,60\n")

    data_str = input("Enter your data here: ")
    print("\n")
    
    sales_data = data_str.split(',')
    sales_data = validate_data(sales_data)
    print('Completed. \n')

    return sales_data


def validate_data(values):
    '''
    Total values is 6
    All values should be able to convert to integer
    '''
    try:
        new_data = [int(value) for value in values]
        if (len(values)) != 6:
            raise ValueError(f"Eactly 6 values required, you provided {len(values)} values")
    
        return new_data
    except ValueError as e:
        print(f"Invalid data: {e}, try again. \n")
        get_sales_data()


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided
    """
    print("Updating sales worksheet... \n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)

    print("Sales worksheet appended successfully... \n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print('Calculating Surplus Data... \n')
    stock = SHEET.worksheet('stock').get_all_values()
    
    stock_row = stock[-1]
    surplus_row = []

    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_row.append(surplus)

    return surplus_row

def main():
    sales_data = get_sales_data()
    update_sales_worksheet(sales_data)
    surplus = calculate_surplus_data(sales_data)


if __name__ == "__main__":
    main()
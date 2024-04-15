import csv

def read_csv_as_2d_array(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            # Strip whitespaces from each element in the row
            row = [element.strip() for element in row]
            data.append(row)
    return data

def remove_row_from_csv(file_path, row_to_remove):
    # Read the CSV data and store it in a list of lists
    data = []
    with open(file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(row)

    # Identify and remove the row to delete from the list
    try:
        data.remove(row_to_remove)
    except ValueError:
        print("Row not found in the CSV file.")

    # Write the modified data back to the CSV file, overwriting the existing content
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)
      
def is_in_one_percent_of(num1, num2):
    one_percent_of_num2 = (3 / 100) * abs(num2)  # Use abs() to handle negative values
    return (num2 - one_percent_of_num2) <= num1 <= (num2 + one_percent_of_num2)

csv2 = read_csv_as_2d_array('csv2.csv')
csv1 = read_csv_as_2d_array('csv1.csv')

c = 0
match_found = False
      

merged_data = {}  # To store the merged rows (dictionary with a unique key as the identifier)
duplicate_rows = []  # To store the duplicate rows

for row in csv2:
    # Flag to indicate if the current row has duplicates
    has_duplicates = False

    for row2 in csv2:
        if row is not row2:  # Ensure it's not the same row
            if row[0] == row2[0] and row2[1] == row[1] and row2[2] == row[2] and row2[3] != row[3] and row2[4] != row[4]:
                # If it's a duplicate, calculate the average values
                money1 = float(row[5].replace("$", "").replace(",", ""))
                money2 = float(row2[5].replace("$", "").replace(",", ""))
                bet1 = float(row[4])
                bet2 = float(row2[4])
                avg_money = (money1 * bet1 + money2 * bet2) / (bet1 + bet2)
                avg_pnl = (avg_money - bet1) / abs(bet1) * 100  # Calculate the average pnl

                # Create a new row with the averaged values
                new_row = row.copy()
                new_row[4] = bet1 + bet2  # Update the total bet
                new_row[5] = "${:,.2f}".format(avg_money)  # Update the average money as a formatted string
                new_row[6] = "${:,.2f}".format(avg_pnl)  # Update the average pnl as a formatted string
                
                # Store the new row in the merged_data dictionary with a unique key
                key = tuple(new_row[:7])  # Use the first 7 elements of the row as the key
                merged_data[key] = new_row
                remove_row_from_csv('csv2.csv', row2)

                # Mark the current row as having duplicates
                has_duplicates = True

    # If the current row doesn't have duplicates, store it in the duplicate_rows list
    if not has_duplicates:
        duplicate_rows.append(row)

# Print the merged data to verify the results
for row in merged_data.items():
    print(row)





for row in csv2:
    counter = 0
    match_found = False
    for row2 in csv1:
        if row[0] == "Date:" or row2[1] == "Book" or row[2] != "Basketball":
            pass
        else:
            match1 = False
            match2 = False
            match3 = False
            finalmatch = False
            date = row[0]
            if date in row2[3]:
                match1 = True

            matchup = row[1].split('/')
            team1 = matchup[0]
            team2init = matchup[1].split(" ")
            team2 = team2init[0]
            if team1  == "LAL":
              team1 = "Lakers"
            if team1  == "LAC":
              team1 = "Clippers"
            if team1  == "PHO":
              team1 = "PHX"
            if team1  == "SAS":
              team1 = "SA"
            if team1 == "LVA":
              team1 = "Aces"
            if team1 == "LAS":
              team1 = "Sparks"
            if team2 and team1 in row2[4]:
                match2 = True
              

            money1 = row[5]
            money1 = money1.replace("$", "").replace(",", "").split(".")[0]
            money2 = row2[6]
            money1 = float(money1)
            money2 = float(money2)


            bet = team2init[2]
            if 'o' in bet:
                type_bet = "over"
            else:
                type_bet = "under"
            bet = bet.replace("u", "").replace("o", "")

            bet2 = row2[5]
            bet2 = bet2.split(" ")

            over_under = bet2[2]
            betodds2 = bet2[3]
            bet = float(bet)
            betodds2 = float(betodds2)


            if bet == betodds2:
                match3 = True
            if match3 == True and match2 == True and match1 == True:
                finalmatch = True
                match_found = True

            risk1 = row[3]
            risk2 = row2[9]
            risk1 = risk1.split('.')[0]
            risk2 = risk2.split('.')[0]

            pnl1 = float(row[4])
            pnl2 = float(row2[8])
            pnltf = is_in_one_percent_of(pnl2, pnl1)
            risttf = is_in_one_percent_of(int(risk1), int(risk2))
            moneytf = is_in_one_percent_of((money2*2), money1)

            if row2[12] == "WIN":
                wl2 = 'W'
            else:
                wl2 = 'L'
            printrow = False
            if finalmatch == True:
                if moneytf == False:
                    print('Money mismatch error!')
                    printrow = True
                if risttf == False:
                    print('Risk error!')
                    print(risk1)
                    print(risk2)
                    printrow = True
                if wl2 != row[8]:
                    print("W/L error!")
                    printrow = True
                if pnltf != True:
                    print("PNL error!")
                    printrow = True

                if printrow == True:
                    print(row)
                    print(row2)
                    print('\n')




    if not match_found and row[0] != "Date:" and row[2] == "Basketball":
        if counter == 0:
            print('Match not found for master:')
            print(row)
            print(row2)
            counter += 1
            print('\n')

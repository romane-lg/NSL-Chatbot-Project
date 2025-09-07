# %%
def main():

    # Initiate Code
    welcome_phase()

if __name__ == '__main__':
  main()

# %% [markdown]
# \# 1. Configuration & Initial Data Import
# 

# %%
import pandas as pd
import json

#Loading appropriate dictionarries for each team
TEAMS_DICT = {
    "1": "Montreal Roses",
    "2": "Vancouver Rise FC",
    "3": "Calgary Wild FC",
    "4": "AFC Toronto",
    "5": "Halifax Tides FC",
    "6": "Ottawa Rapid FC"
}

TEAMS_INFO = {
    "AFC Toronto": {
        "Founded": 2023,
        "Home City": "Toronto, Ontario",
        "Home Stadium": "York Lions Stadium",
        "Colors": "Maroon and vermillion",
        "Motto": "Rise up!",
        "Head Coach": "Marko Milanović"
    },
    "Calgary Wild FC": {
        "Founded": 2024,
        "Home City": "Calgary, Alberta",
        "Home Stadium": "McMahon Stadium",
        "Colors": "Red and violet",
        "Motto": "She shoots, she soars!",
        "Head Coach": "Lydia Bedford"
    },
    "Halifax Tides FC": {
        "Founded": 2024,
        "Home City": "Halifax, Nova Scotia",
        "Home Stadium": "Wanderers Grounds",
        "Colors": "Ocean cyan, marine purple, ship grey",
        "Motto": "Rise Together",
        "Head Coach": "Stephen Hart (interim, as of June 2025)"
    },
    "Montreal Roses": {
        "Founded": 2023,
        "Home City": "Laval (Montreal area), Quebec",
        "Home Stadium": "Stade Boréale (Laval)",
        "Colors": "Black, blue, gold, red, white",
        "Motto": "Making the impossible, possible.",
        "Head Coach": "Robert Rositoiu"
    },
    "Ottawa Rapid FC": {
        "Founded": 2024,
        "Home City": "Ottawa, Ontario",
        "Home Stadium": "TD Place Stadium",
        "Colors": "Light blue (primary), orange accent, white",
        "Motto": "Rapid Change. Enduring Legacy.",
        "Head Coach": "Katrine Pedersen"
    },
    "Vancouver Rise FC": {
        "Founded": 2022,
        "Home City": "Burnaby, British Columbia",
        "Home Stadium": "Swangard Stadium",
        "Colors": "Teal, black, gold",
        "Motto": "Rise to the occasion.",
        "Head Coach": "Anja Heiner-Møller"
    }
}

# Utility function to load CSV files with defensive programming.
# Returns an empty DataFrame instead of raising an exception,
# ensuring downstream code can still execute without breaking.

def read_csv_safe(path, encoding):
    """
    Reads a CSV file into a Pandas DataFrame with error handling.

    """
    try:
        return pd.read_csv(path, encoding=encoding)
    except FileNotFoundError:
        # If the file path is invalid or missing
        print(f"Error: The file '{path}' was not found.")
    except UnicodeDecodeError:
        # If the encoding does not match file format
        print(f"Error: Could not decode '{path}' with encoding '{encoding}'.")
    # Return an empty DataFrame so the program doesn't crash
    return pd.DataFrame()

# Main data-loading function.
# Aggregates static dictionaries and external CSV data into a single
# cohesive dictionary for centralized access by other functions.
def import_files():
    # Load primary datasets from disk using a safe loader
    team_roster_df = read_csv_safe("all_players.csv", "latin-1")   # Player roster
    account_df = read_csv_safe("customer_database.csv", "utf-8")  # User accounts
    created_teams_df = read_csv_safe("created_teams.csv", "utf-8")  # User-generated fantasy teams

    # Initialize account dictionary
    account_dict = {}

    # If account data loaded successfully, convert it to a dict for faster lookups
    if not account_df.empty and "customer_id" in account_df.columns:
        account_dict = account_df.set_index('customer_id').to_dict('index')

    return {
        "teams_dict": TEAMS_DICT,             # Static team ID-to-name mapping
        "teams_info": TEAMS_INFO,             # Rich team metadata
        "team_roster_df": team_roster_df,     # Players and their details
        "account_dict": account_dict,         # User account info (dict form)
        "created_teams_df": created_teams_df  # Fantasy team creations
    }

# %% [markdown]
# # 2. Main Chatbot Application Flow
# 

# %%
def welcome_phase():
    """
    Greet the user, and routing them to a primary feature based on their main menu selection.
    """

    # Welcome
    print_welcome_message()

    # Get user name
    user_name = input('Enter your name here: ').strip()
    print(f"\nFantastic {user_name}! I'm so glad to meet you!\n" + "-"*54)
    first_phase(user_name)

def first_phase(user_name):

    # Load all datasets once
    my_datasets = import_files()
    teams_dict = my_datasets.get('teams_dict', {})
    teams_info = my_datasets.get('teams_info', {})
    team_roster_df = my_datasets.get('team_roster_df', pd.DataFrame())
    account_dict = my_datasets.get('account_dict', {})


    # Menu options mapped to functions (no lambda)
    menu_actions = {
        '1': discover_teams_players,
        '2': start_fantasy_team
    }

    print_menu()

    while True:
        choice = input('Input the number corresponding to your choice: ').strip()
        if choice in menu_actions:
            menu_actions[choice](user_name, teams_dict, teams_info, team_roster_df, account_dict)
            break
        else:
            print('Please enter a valid choice.')


def print_welcome_message():
    print("""Hello! Welcome to the NSL Stats Chatbot!
-------------------------------------------------------
I am here to help you learn more about the players and teams of the Northern Super League.
Tell me your name first so I can get to know you better!
""")


def print_menu():
    print("""
What can I help you with today?
1. Discover the teams and players
2. Start a Fantasy Team
""")


def discover_teams_players(user_name, teams_dict, teams_info, team_roster_df, account_dict):
    discover_phase(user_name, teams_dict, teams_info, team_roster_df)


def start_fantasy_team(user_name, teams_dict, teams_info, team_roster_df, account_dict):
    fantasy_phase(user_name, account_dict, team_roster_df)

# %% [markdown]
# # 3. Feature: NSL Information Discovery
# 

# %% [markdown]
# ###  3.1 Team Discovery Functions

# %%
def discover_phase(user_name, teams_dict, teams_info, team_roster_df):
    """
    Routes the user to either the team discovery or player discovery function based on their selection from a sub-menu.
    """
    # Greet the user and explain the discovery options
    print(f"Okay {user_name} let's help you get to know more about the players and teams!")
    print(f"""What would you like to discover?
1. Teams
2. Players""")

    # Map user input numbers to their corresponding discovery category
    dic = {'1': 'Teams',
           '2': 'Players'}

    while True:
        # Ask the user for their choice
        user_choice = input('Input the number corresponding to your choice. I want to know more about:')

        # If the choice is valid, call the appropriate function
        if user_choice in dic.keys():
            if user_choice == '1':
                favourite_team(user_name, teams_dict, teams_info, team_roster_df)  # Explore teams
                break
            else:
                favourite_players(user_name, team_roster_df)  # Explore players
                break
        else:
            # Invalid input → prompt again
            print('Please enter a valid choice')

# %%
def post_search_menu(user_name):
    """Handles the menu after a search to return to main menu or exit."""
    while True:
        menu_choice = input("Would you like to return to the main menu (1) or exit (2)? ")
        if menu_choice == '1':
            first_phase(user_name)
            return True  # Signal to exit current function
        elif menu_choice == '2':
            print("\n Thank you, Goodbye!")
            return True  # Signal to exit current function
        else:
            print("Invalid choice. Please enter 1 or 2.")
    return False

# %%
def favourite_team(user_name, teams_dict, teams_info, team_roster_df):
    """
    Prompts the user to select a team and automatically displays its organizational info.
    The user can then choose to look up another team or return to the main menu/exit.
    """
    # This loop allows the user to look up multiple teams until they choose to stop.
    while True:
        print("\n---------------------------------------------------")
        # Dynamically generate the team list from the dictionary.
        for team_id, team_name in teams_dict.items():
            print(f"{team_id}. {team_name.split(' FC')[0]}")
        print("---------------------------------------------------")

        user_favourite_team = input("What is your favourite team? (Insert the corresponding number):").strip()

        # Check if the user's input is a valid team ID.
        if user_favourite_team in teams_dict:
            team_name = teams_dict[user_favourite_team]

            #Print the team profile
            print(f"\nTeam profile of {team_name}:\n")
            for key, value in teams_info[team_name].items():
                print(f"{key}: {value}")
            another_search = input("\nWould you like to look up another team? (yes/no): ").strip().lower()
            while another_search not in ['yes','no']:
                print("\nInvalid choice. Please enter 'yes' or 'no'.")
                another_search = input("\nWould you like to look up another team? (yes/no): ").strip().lower()
            if another_search == "no":
                print("\nThank you for using the team information tool!")
                # Give the option to go to the main menu or exit the program entirely.
                if post_search_menu(user_name):
                    return # The return exits the favourite_team function.
                break # This break exits the main 'while' loop, also ending the function.
            else:
                continue


        else:
            print("Invalid team selection. Please choose a valid team number.")

# %% [markdown]
# ## 3.2 Player Discovery Functions

# %%
import plotly.express as px
from IPython.display import display  # for inline, non-blocking map in Colab

def favourite_players(user_name, team_roster_df):
    """
    Handles the main menu and logic for searching players from the roster.
    Works with input() for all interactions.
    """
    while True:
        # Show the main menu
        print(f"""\nGreat option! How would you like to know more about the NSL league players?
1. Search by player name or position (Goalkeeper, Defender, Midfielder, Forward)
2. Find a player from my favourite country""")

        input_choice = input('Input the number corresponding to your choice here:').strip()

        # ---------------------- OPTION 1 ----------------------
        if input_choice == '1':
            while True:
                player_choice = input('Enter the full player name or position: ').title().strip()
          #check if the name entered is in the dataset of players and print the player profile card
                if player_choice in team_roster_df['name'].values:
                    player_data = team_roster_df.loc[team_roster_df['name'] == player_choice].iloc[0]
                    print(f""" | Player Profile |
==========================================================
- Name: {player_data['name']}
- Team: {player_data['team']}
- Position: {player_data['position']}
- Nationality: {player_data['nationality']}""")
                #repeat the same process but with the position
                elif player_choice in team_roster_df['position'].values:
                    filtered_players = team_roster_df[team_roster_df['position'] == player_choice]
                    print(f"\n| All Players with the position: {player_choice} |")
                    print("==========================================================")
                    for _, row in filtered_players.iterrows():
                        print(f"Name: {row['name']}, Team: {row['team']}")
              #error handling if the player is not in the dataset
                else:
                    print("\nSorry, that's not a valid player name or position.")
                    continue

                another_search = input("\nWould you like to look up another player or position? (yes/no): ").strip().lower()
                while another_search not in ['yes', 'no']:
                    print("Please enter 'yes' or 'no'.")
                    another_search = input("Would you like to look up another player or position? (yes/no): ").strip().lower()
                if another_search == 'no':
                    if post_search_menu(user_name):
                        return
                    break
            continue

        # ---------------------- OPTION 2 ----------------------
        elif input_choice == '2':
            # ---- Clean the nationality column first ----
            team_roster_df['nationality'] = team_roster_df['nationality'].str.strip().str.lower()

            # ---- Show world map ----
            country_counts = team_roster_df['nationality'].value_counts().reset_index()
            country_counts.columns = ['country', 'count']

            fig = px.choropleth(
                country_counts,
                locations="country",
                locationmode="country names",
                color="count",
                hover_name="country",
                color_continuous_scale=px.colors.sequential.Plasma,
                title="Spread of NSL Players by Country"
            )

            # Use Colab-friendly renderer so input() function works after the map appears
            fig.show(renderer="colab")

            # ---- Ask user for country ----
            while True:
                input_country_clean = input('Enter the full country name you are interested in: ').strip().lower()

                filtered_players = team_roster_df[
                    team_roster_df['nationality'] == input_country_clean
                ]

                if not filtered_players.empty:
                    print(f"\n| All Players from {input_country_clean.title()} |")
                    print("==========================================================")
                    for _, row in filtered_players.iterrows():
                        print(f"Name: {row['name']}, Team: {row['team']}")
                else:
                    print(f"\nNo players found from '{input_country_clean.title()}'. Please enter the full country name.")
                    continue
                #ask if user want to ask another question in the country option
                another_search = input("\nWould you like to search for another country? (yes/no): ").strip().lower()
                while another_search not in ['yes', 'no']:
                    print("Please enter 'yes' or 'no'.")
                    another_search = input("Would you like to search for another country? (yes/no): ").strip().lower()
                if another_search == 'no':
                    if post_search_menu(user_name):
                        return
                    break
            continue

        # ---------------------- Invalid Menu Choice ----------------------
        else:
            print("\nThat’s not a valid choice. Please enter 1 or 2.")
            continue

# %% [markdown]
# # 4. Feature: Fantasy Team Management
# 

# %% [markdown]
# ## 4.1 User Authentication Functions

# %%
def fantasy_phase(user_name, account_dict, team_roster_df):
  """
  Initiates the fantasy team workflow by prompting the user for their email to either log in or create a new account.
  """
  # Display welcome message fo Fantasy phase
  print(f"Okay {user_name}  let's help you start a Fantasy Team! First, let's log in or create an account")
  # Ask user to input email address and check if it exists or not
  email_address = input("Enter your email address: ")

  # Pass created_teams_df to check_identifier
  my_datasets = import_files()
  created_teams_df = my_datasets.get('created_teams_df', pd.DataFrame())
  check_identifier(user_name, email_address, account_dict, created_teams_df) # Pass created_teams_df

# %%
def check_identifier(user_name, identifier, customer_database, created_teams_df): # Accept created_teams_df
  """
  Checks if a user's email exists in the database, triggering a login for an existing user or creating a new account for a new user.
  """
  while True:
      # Create a copy to iterate over
      for key, value in list(customer_database.items()):
          if value['email'].lower() == identifier.lower() :
              pin = value['pin']
              name = value['name']
              customer_id = key
              login_account_with_pin(user_name, pin, name, customer_id, created_teams_df) # Pass created_teams_df
              return # Exit the function after finding the identifier
      # If the loop finishes without finding the identifier, create a new customer
      pin = create_pin(identifier, user_name)
      customer_id = f"customer{len(customer_database)+1}"
      customer_database[customer_id] = {}
      customer_database[customer_id]['name'] = user_name
      customer_database[customer_id]['email'] = identifier
      customer_database[customer_id]['pin'] = pin
      save_customer_database(customer_database) # Save the updated database
      instructions(user_name, customer_id, created_teams_df) # Pass created_teams_df
      return # Exit the function after creating a new customer

# %%
def login_account_with_pin(user_name, correct_pin, name, customer_id, created_teams_df): # Accept created_teams_df
  """
  Authenticates an existing user by verifying their entered PIN against the correct one, granting access upon success or redirecting after multiple failures.
  """
  import getpass


    # turn pin into a string to match with input
  correct_pin_str = str(correct_pin)

  while True:
          # To take into account security
          # Max attemps: 3 times (as per standard)
          max_attempts  = 3
          # Set counter
          attempts = 0
          while attempts < max_attempts:
              # Prompt user to input 4 digit pin securely (with hash)
              # getpass is used to hide the input for security
              pin_input = getpass.getpass(f"{name}, please enter your 4-digit pin to enter your account: ")

              # 4 digit pin must match the correct_pin
              if pin_input == correct_pin_str:
                  print(f"Welcome, {name}!")
                  instructions(user_name, customer_id, created_teams_df)

                  return True  # Login successful, exit the function
              else:
                  attempts += 1
                  if attempts < max_attempts:
                    print("Invalid PIN. Please try again or contact customer service for assistance.")
                  else:
                      print(f"You have have reached the maximum number of attemps ({max_attempts}) and are locked out.Please try again or contact customer service for assistance.")
                      return False

# %%
def create_pin(email_address, name):
  """
  Prompts a new user to create and confirm a 4-digit numerical PIN, validating the input before returning the successfully created PIN.
  """
  import getpass
      # prompt identifier until identifier is in customer_database
  while True:
        pin = getpass.getpass(f"{name.title()}, please enter a 4 digit pin to complete your registration: ")
        if pin.isdigit() and len(pin) == 4:
            print(f'Your pin has been created. Thank you')
            return pin  # valid, exit loop
        else:
            print("Invalid PIN. Please enter a 4 digit pin.")


# %% [markdown]
# ## 4.2 Team Creation & Recommendation Functions

# %%
def instructions(user_name, customer_id,created_teams_df):
  """
  Guides the user into the team creation process by displaying instructions and then calling the recommendation function.
  """
  print(f"""
  ===================================
          WELCOME TO TEAM BUILDER!
  ===================================

  It's time to create your dream squad.
  Your goal: choose the perfect lineup by selecting players
  for each position based on the attributes you value most.

  How it works:
  - Team size: 11 players total
  - Formation: 1 Goalkeeper, 4 Defenders, 3 Midfielders, 3 Forwards
  - Player attributes: Each player has unique strengths based on their stats.
  - Your role: Enter your top desired attributes, and we'll suggest
    players who match your preferences.

  Get ready to balance skill, strategy, and style—
  your winning team starts here!
  """)

  customer_id = customer_id

  # Calling the function to display the current team, or fill/modify the current team
  display_team(user_name,customer_id,created_teams_df)


# %%
def display_team(user_name, customer_id, created_teams_df):

    import pandas as pd
    import json

    # Call the import function once to get all the data
    my_datasets_created_teams = import_files()
    # Get team roster data
    team_roster_df = my_datasets_created_teams.get('team_roster_df', pd.DataFrame())


    # Check if the customerid exists as a key in the created_teams_df

    if 'customer_id' in created_teams_df.columns and customer_id not in created_teams_df['customer_id'].values:
        customer_team_df = pd.DataFrame(columns=["customer_id", "position", "playername", "qualities"]) # Initialize empty DataFrame


        # Call for the recommendation function for new team creation
        recommendation(user_name,customer_id,customer_team_df, team_roster_df, created_teams_df) # Pass created_teams_df

    else:
        print("\nCurrent Team:")
        # Print created teams df
        # Filter the DataFrame to show only the current customer's team
        if 'customer_id' in created_teams_df.columns:
             customer_team_df = created_teams_df[created_teams_df['customer_id'] == customer_id].copy() # Create a copy to avoid SettingWithCopyWarning


             # If customer has an existing team
             if not customer_team_df.empty:
              with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                display_df = customer_team_df.drop(columns='customer_id').set_index('position')
                # Rename columns and index
                display_df = display_df.rename(columns={
                    'playername': 'Player Name',
                    'qualities': 'Qualities'
                      })
                display_df.index.name = 'Position'
                print(display_df.to_string())

                # Start recommendation function to allow the modification
                recommendation(user_name,customer_id,customer_team_df, team_roster_df, created_teams_df) # Pass created_teams_df
             else:
                # Customer ID exists in column but has no team rows
                 message = "\nLooks like you don't have a team yet, please create one"
                 print(message)
                 customer_team_df = pd.DataFrame(columns=["customer_id", "position", "playername", "qualities"]) # Initialize empty DataFrame
                 recommendation(user_name,customer_id,customer_team_df, team_roster_df, created_teams_df) # Pass created_teams_df
        else:
             print("Error: 'customer_id' column not found in created_teams_df")


def recommendation(user_name, customer_id,customer_team_df, team_roster_df, created_teams_df): # Accept created_teams_df

    # Define key qualities for each player position
    qualities = {
        "Goalkeeper": ['Shot-Stopping','Handling','Commanding the Box','Distrbution','Resilience','Decision-Making'],
        "Defender": ["Tackling", "Interception", "Marking", "Clearances", "Positioning", "Communication"],
        "Midfielder": ["Passing", "Dribbling", "Ball control", "Shooting", "Tackling & Interceptions", "Crossing"],
        "Forward": ["Finishing", "Ball Control", "Dribbling", "Shooting Power", "Movement Off the Ball", "Stamina"]
    }

    # Map user input numbers to positions
    positions = {
        "1": "Goalkeeper",
        "2": "Defender",
        "3": "Midfielder",
        "4": "Forward",
        "5": "Exit"
    }

    if customer_team_df is None:
        customer_team_df = pd.DataFrame(columns=["customer_id", "position", "playername", "qualities"])

    # Begin team modification loop
    while True:

        # Ask user which position to modify
        print("\nWhich position would you like to fill / modify?")
        print("\n1. Goalkeeper\n2. Defender\n3. Midfielder\n4. Forward\n5. I'm happy with my team")
        user_input = input("Enter your choice: ").strip()

        if user_input in positions:
            if user_input == "5":
              # If user is done editing
              print("\nTeam finalized:\n")
              if customer_team_df is not None and not customer_team_df.empty:
                with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                  display_df = customer_team_df.drop(columns='customer_id').set_index('position')
                # Rename columns and index
                  display_df = display_df.rename(columns={
                    'playername': 'Player Name',
                    'qualities': 'Qualities'
                      })
                  display_df.index.name = 'Position'
                  print(display_df.to_string())
              else:
                print("Looks like you don't have a team yet, please create one")
                continue
              break
            else:
                # Ask for quality selection for the chosen position
                position = positions[user_input].strip()
                print(f"\nWhat is the most desirable quality you would like your {position}s to possess?")

                # List available qualities for that position
                for i, q in enumerate(qualities[position], 1):
                    print(f"{i}. {q}")

                # Handle user input for quality selection
                while True:
                    try:
                        choice = int(input("\nEnter the number of your chosen quality: "))
                        if 1 <= choice <= len(qualities[position]):
                            chosen_quality = qualities[position][choice - 1]  # Get the quality from the list
                            break
                        else:
                            print("\nInvalid selection. Try again.")
                    except ValueError:
                        print("\nPlease enter a number.")

                # Ask for a second quality selection for the chosen position
                print(f"\nWhat is the other quality you would like your {position}s to possess?")

                # List available qualities for that position
                for i, q in enumerate(qualities[position], 1):
                    print(f"{i}. {q}")

                # Handle user input for quality selection
                while True:
                    try:
                        choice2 = int(input("\nEnter the number of your chosen quality: "))
                        if 1 <= choice2 <= len(qualities[position]):
                            chosen_quality2 = qualities[position][choice2 - 1]  # Get the quality from the list
                            break
                        else:
                            print("\nInvalid selection. Try again.")
                    except ValueError:
                        print("\nPlease enter a number.")

                # Combine qualities with pipe separator
                combined_qualities = f"{chosen_quality} | {chosen_quality2}"

                position_counts = {
                    "Goalkeeper": 1,
                    "Defender": 4,
                    "Midfielder": 3,
                    "Forward": 3
                    }

                required_count = position_counts.get(position, 1)
                # Get top N players matching the selected qualities
                top_players = get_top_players(position, combined_qualities, team_roster_df, top_n=required_count)

                if top_players.empty:
                  print(f"No matching players found for position {position} with qualities: {combined_qualities}")
                  continue
                # Remove existing players for this position and customer
                if customer_team_df is None:
                    customer_team_df = pd.DataFrame()
                else:
                    customer_team_df = customer_team_df[~(
                        (customer_team_df["customer_id"] == customer_id) &
                        (customer_team_df["position"] == position)
                    )].copy() # Create a copy to avoid SettingWithCopyWarning


                # Create new rows for the selected top players
                new_rows = []
                for _, row in top_players.iterrows():
                    new_rows.append({
                        "customer_id": customer_id,
                        "position": position,
                        "playername": row["name"],
                        "qualities": combined_qualities
                    })

                # Append the new players
                customer_team_df = pd.concat([customer_team_df, pd.DataFrame(new_rows)], ignore_index=True)

                # Get top players
                top_players = get_top_players(position, combined_qualities, team_roster_df, top_n=required_count)

                if top_players.empty:
                  print(f"No matching players found for position {position} with qualities: {combined_qualities}")
                  continue  # Skip to next loop

                # Remove existing players for this customer and position (in case they’re updating)
                if customer_team_df is not None and not customer_team_df.empty:
                  customer_team_df = customer_team_df[~((customer_team_df['customer_id'] == customer_id) &
                          (customer_team_df['position'] == position))].copy() # Create a copy to avoid SettingWithCopyWarning

                # Create new rows for each selected player
                new_rows = []
                for _, row in top_players.iterrows():
                  new_row = {
                      "customer_id": customer_id,
                      "position": position,
                      "playername": row['name'],  # Uses 'name' from team_roster_df
                      "qualities": combined_qualities
                      }
                  new_rows.append(new_row)

                # Append to or create customer_team_df
                new_rows_df = pd.DataFrame(new_rows)
                if customer_team_df is None or customer_team_df.empty:
                  customer_team_df = new_rows_df
                else:
                  customer_team_df = pd.concat([customer_team_df, new_rows_df], ignore_index=True)

        else:
            print("\nInvalid input. Please choose a number from 1 to 5.")

    # Offer next action after team is finalized
    save_created_teams(customer_team_df)
    print("\n")
    post_search_menu(user_name)


    return customer_team_df

# %%
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_top_players(position, desired_qualities, team_roster_df, top_n=1):
    # Filter only for relevant position
    position_players = team_roster_df[team_roster_df['position'] == position].copy()

    # Check if position_players is empty or if 'attributes' column exists
    if position_players.empty or 'attributes' not in position_players.columns:
        print(f"No players found for position: {position} or 'attributes' column is missing.")
        return pd.DataFrame() # Return empty DataFrame

    # Vectorize the qualities with | as a separator
    vectorizer = CountVectorizer(tokenizer=lambda x: x.split('|'), token_pattern=None)
    qualities_matrix = vectorizer.fit_transform(position_players['attributes'].dropna()) # Handle potential NaN values

    # Transform user-desired qualities
    desired_vector = vectorizer.transform([desired_qualities])

    # Compute cosine similarity
    similarity_scores = cosine_similarity(desired_vector, qualities_matrix).flatten()

    # Add similarity scores to DataFrame
    position_players['similarity'] = similarity_scores

    # Sort and return top N
    top_players = position_players.sort_values(by='similarity', ascending=False).head(top_n)

    return top_players[['name', 'position', 'attributes', 'similarity']] # Use 'name' for team_roster_df

# %% [markdown]
# # 5. Data Persistence Utilities
# 

# %%
def save_customer_database(customer_database, filename='/content/customer_database.csv'):
    """
  Converts the provided customer database dictionary into a DataFrame and saves it to a specified CSV file.
  """
    import csv

    #Saves the customer database dictionary to a CSV file.
    with open(filename, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)

        # Write the header row
        # Assuming all customer dictionaries have the same keys
        if customer_database:
            header = ['customer_id'] + list(next(iter(customer_database.values())).keys())
            writer.writerow(header)

            # Write the data rows
            for customer_id, data in customer_database.items():
                row = [customer_id] + list(data.values())
                writer.writerow(row)
        else:
            # Write only the header if the database is empty
            writer.writerow(['customer_id', 'email', 'name', 'pin'])

# %%




#####| Imports and Constants: |#####
import os
import threading
import json
import requests
from io import BytesIO
from datetime import datetime
from PIL import Image
import colorama
from colorama import Fore, Style
import sqlite3
import time

colorama.init(autoreset=True)

MSG_USER_EXISTS = "User already exists in the database. Skipping insertion."
MSG_DATA_INSERTED = "Data inserted into the database."
MSG_NO_CHANGES = "No changes detected in the database."
MSG_CHANGES_DETECTED = "Changes detected in the database."
MSG_USER_NOT_FOUND = "User not found in the database."
MSG_UNABLE_TO_RETRIEVE = "Unable to retrieve {}."

#####| Funções Relacionadas ao Banco de Dados - Database Related Functions|#####

def create_table():
    conn = sqlite3.connect('instagram_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS instagram_profiles (
            user_id TEXT PRIMARY KEY,
            username TEXT,
            profile_picture_url TEXT,
            bio TEXT,
            num_posts INTEGER,
            num_followers INTEGER,
            num_following INTEGER,
            external_url TEXT,
            full_name TEXT,  -- New field for full name
            facebook_url TEXT,  -- New field for Facebook URL
            is_private INTEGER,  -- New field for is_private
            is_verified INTEGER,  -- New field for is_verified
            business_address TEXT,  -- New field for business address
            business_contact_method TEXT,  -- New field for business contact method
            business_email TEXT,  -- New field for business email
            business_phone_number TEXT,  -- New field for business phone number
            business_category_name TEXT,  -- New field for business category name
            overall_category_name TEXT,  -- New field for overall category name
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

create_table()

# Função para verificar se o usuário já existe no banco de dado - Function to check if the user already exists in the database #
def user_exists_in_db(user_id):
    conn = sqlite3.connect('instagram_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 1 FROM instagram_profiles WHERE user_id = ?
    ''', (user_id,))

    exists = cursor.fetchone() is not None

    conn.close()

    return exists

# Função para inserir dados no banco de dados -  Function to insert data into the database #
def insert_data_to_db(user_id, username, profile_picture_url, bio, num_posts, num_followers, num_following, external_url,
                       full_name, facebook_url, is_private, is_verified,
                       business_address, business_contact_method, business_email,
                       business_phone_number, business_category_name, overall_category_name):
    conn = sqlite3.connect('instagram_data.db')
    cursor = conn.cursor()

    if user_exists_in_db(user_id):
        print_colored("User already exists in the database. Skipping insertion.", Fore.YELLOW)
    else:
        cursor.execute('''
            INSERT INTO instagram_profiles
            (user_id, username, profile_picture_url, bio, num_posts, num_followers, num_following, external_url,
            full_name, facebook_url, is_private, is_verified,
            business_address, business_contact_method, business_email,
            business_phone_number, business_category_name, overall_category_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, username, profile_picture_url, bio, num_posts, num_followers, num_following, external_url,
              full_name, facebook_url, is_private, is_verified,
              business_address, business_contact_method, business_email,
              business_phone_number, business_category_name, overall_category_name))

        print_colored("Data inserted into the database.", Fore.GREEN)

    conn.commit()
    conn.close()

# Função para atualizar dados no banco de dados - Function to update data in the database #
def update_data_in_db(user_id, username, profile_picture_url, bio, num_posts, num_followers, num_following, external_url,
                       full_name, facebook_url, is_private, is_verified,
                       business_address, business_contact_method, business_email,
                       business_phone_number, business_category_name, overall_category_name):
    conn = sqlite3.connect('instagram_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE instagram_profiles
        SET username=?, profile_picture_url=?, bio=?, num_posts=?, num_followers=?, num_following=?, external_url=?,
            full_name=?, facebook_url=?, is_private=?, is_verified=?,
            business_address=?, business_contact_method=?, business_email=?,
            business_phone_number=?, business_category_name=?, overall_category_name=?,
            last_updated=CURRENT_TIMESTAMP
        WHERE user_id=?
    ''', (username, profile_picture_url, bio, num_posts, num_followers, num_following, external_url,
          full_name, facebook_url, is_private, is_verified,
          business_address, business_contact_method, business_email,
          business_phone_number, business_category_name, overall_category_name, user_id))

    print_colored("Data updated in the database.", Fore.GREEN)

    conn.commit()
    conn.close()

# Função para verificar alterações nos dados - Function to check for changes in data #
def check_for_changes_in_db(user_id, username, profile_picture_url, bio, num_posts, num_followers, num_following, external_url):
    conn = sqlite3.connect('instagram_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM instagram_profiles WHERE user_id = ?
    ''', (user_id,))

    existing_data = cursor.fetchone()

    if existing_data:
        # Check for changes in each field
        changes_detected = False

        field_names = ['user_id', 'username', 'profile_picture_url', 'bio', 'num_posts', 'num_followers', 'num_following', 'external_url']

        for i, field_name in enumerate(field_names):
            # Skip the profile_picture_url and external_url fields for comparison, as they may not change frequently
            if field_name not in ['profile_picture_url', 'external_url']:
                if existing_data[i] != locals()[field_name]:
                    print_colored(f"{field_name} changed: {existing_data[i]} -> {locals()[field_name]}", Fore.RED)
                    changes_detected = True

        if not changes_detected:
            print_colored(MSG_NO_CHANGES, Fore.GREEN)
        else:
            print_colored(MSG_CHANGES_DETECTED, Fore.YELLOW)
    else:
        print_colored(MSG_USER_NOT_FOUND, Fore.YELLOW)

    conn.close()

#Função para coletar todos os dados da DB - Function to collect all data from DB #
def display_all_data_from_db():
    conn = sqlite3.connect('instagram_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM instagram_profiles
    ''')

    all_data = cursor.fetchall()

    if all_data:
        print("\n" + "=" * 50)
        print(f"{Fore.CYAN}{'User Data from the Database':^50}{Style.RESET_ALL}")
        print("=" * 50)

        for row in all_data:
            print(f"{Fore.YELLOW}\nUser ID: {row[0]}")
            print(f"Username: {row[1]}")
            print(f"Profile Picture URL: {row[2]}")
            print(f"Bio: {row[3]}")
            print(f"Number of Posts: {row[4]}")
            print(f"Number of Followers: {row[5]}")
            print(f"Number of Following: {row[6]}")
            print(f"External URL: {row[7]}")
            print(f"Full Name: {row[8]}")
            print(f"Facebook URL: {row[9]}")
            print(f"Is Private: {bool(row[10])}")
            print(f"Is Verified: {bool(row[11])}")
            print(f"Business Address: {row[12]}")
            print(f"Business Contact Method: {row[13]}")
            print(f"Business Email: {row[14]}")
            print(f"Business Phone Number: {row[15]}")
            print(f"Business Category Name: {row[16]}")
            print(f"Overall Category Name: {row[17]}")
            print(f"Last Updated: {row[18]}{Style.RESET_ALL}")
            print("-" * 50)
    else:
        print_colored("No data found in the database.", Fore.YELLOW)

    conn.close()

#####| Funções de Exibição e Interatividade - Display and Interactivity Functions |#####

def print_banner():
    banner = f"""
{Fore.BLUE}{Style.BRIGHT}
  ██████╗ ██╗  ██╗███████╗██╗   ██╗██╗██████╗ 
 ██╔════╝ ╚██╗██╔╝██╔════╝██║   ██║██║██╔══██╗
 ██║  ███╗ ╚███╔╝ ███████╗██║   ██║██║██║  ██║
 ██║   ██║ ██╔██╗ ╚════██║██║   ██║██║██║  ██║
 ╚██████╔╝██╔╝ ██╗███████║╚██████╔╝██║██████╔╝
  ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚═════╝ 
{Style.RESET_ALL}
"""
    print(banner)

def print_credits():
    credits = f"{Fore.BLUE}{Style.BRIGHT}>>> Script created by @Mr_ofcodyx <<<{Style.RESET_ALL}"
    print(credits)
if __name__ == "__main__":
    print_banner()
    print_credits()

def print_colored(text, color):
    print(f"{color}{text}{Style.RESET_ALL}")

def animate_loading():
    print("Searching", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print()

def spinning_animation():
    spin_chars = ["|", "/", "-", "\\"]
    for _ in range(3):  # Altere o número de giros conforme necessário
        for char in spin_chars:
            print(f"{Fore.YELLOW}{char}", end="", flush=True)
            time.sleep(0.1)
            print("\b \b", end="", flush=True)

#####| Funções de Recuperação e Salvamento de Sessão - Session Recovery and Saving Functions |#####

CONFIG_FILE = "config.txt"
# Chama a função para criar a tabela no início do script - Calls the function to create the table at the beginning of the script #

def save_session_id(session_id):
    with open(CONFIG_FILE, 'w') as config_file:
        config_file.write(session_id)

def load_session_id():
    try:
        with open(CONFIG_FILE, 'r') as config_file:
            session_id = config_file.read().strip()
            return session_id
    except FileNotFoundError:
        return None

#####| Funções de Manipulação de Imagens - Image Manipulation Functions |#####

def save_profile_picture(profile_picture_url, username):
    try:
        response = requests.get(profile_picture_url, stream=True)
        response.raise_for_status()

        # Salvar a imagem em uma pasta
        image_folder = "profile_pictures"
        os.makedirs(image_folder, exist_ok=True)
        image_path = os.path.join(image_folder, f"{username}_profile_picture.jpg")

        # Verificar o tipo de conteúdo da resposta
        content_type = response.headers.get('Content-Type', '').split(';')[0].lower()

        if 'image' in content_type:
            # Open the image and save with good quality
            with open(image_path, 'wb') as img_file:
                for chunk in response.iter_content(chunk_size=8192):
                    img_file.write(chunk)

            return image_path
        else:
            print_colored(f"Error: Unexpected content type '{content_type}'.", Fore.RED)

    except requests.exceptions.RequestException as e:
        print_colored(f"Error during request: {e}", Fore.RED)
    except Exception as e:
        print_colored(f"Error saving profile picture: {e}", Fore.RED)

    return None

#####| Funções de Extração de Dados do Instagram - Instagram Data Extraction Functions |#####

def find_instagram_profile(user_id, session_id):
    url = f"https://i.instagram.com/api/v1/users/{user_id}/info/"
    headers = {
        'User-Agent': 'Instagram 10.3.2 (iPhone7,2; iPhone OS 9_3_3; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/420+',
        'Cookie': f'sessionid={session_id}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        username = user_info['user']['username']
        profile_picture_url = user_info['user']['hd_profile_pic_url_info']['url']
        bio = user_info['user']['biography']
        num_posts = user_info['user']['media_count']
        num_followers = user_info['user']['follower_count']
        num_following = user_info['user']['following_count']
        external_url = user_info['user']['external_url']

        return username, profile_picture_url, bio, num_posts, num_followers, num_following, external_url
    else:
        return None

def find_instagram_id_by_username(username):
    url = f"https://www.instagram.com/{username}/"
    response = requests.get(url)
    if response.status_code == 200:
        user_id_start = response.text.find('"profilePage_', 0) + len('"profilePage_')
        user_id_end = response.text.find('"', user_id_start)
        user_id = response.text[user_id_start:user_id_end]
        return user_id
    else:
        return None

def extract_instagram_data(username, session_id):
    url = 'https://www.instagram.com/api/v1/users/web_profile_info/'
    params = {'username': username}

    headers = {
        'User-Agent': 'Instagram 10.3.2 (iPhone7,2; iPhone OS 9_3_3; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/420+',
        'Cookie': f'sessionid={session_id}'
    }

    response = requests.get(url, params=params, headers=headers)

    try:
        response.raise_for_status()
        data = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        print_colored(f"Error during request: {e}", Fore.RED)
        return None
    except json.JSONDecodeError as e:
        print_colored(f"Error decoding JSON: {e}", Fore.RED)
        return None

    user_data = data.get('data', {}).get('user', {})

    if user_data is not None:
        # Extrair os campos desejados
        full_name = user_data.get('full_name', '')
        fb_profile_biolink = user_data.get('fb_profile_biolink', {})
        facebook_url = fb_profile_biolink.get('url', '') if isinstance(fb_profile_biolink, dict) else ''
        is_private = user_data.get('is_private', False)
        is_verified = user_data.get('is_verified', False)
        business_address_json = user_data.get('business_address_json', None)
        business_contact_method = user_data.get('business_contact_method', '')
        business_email = user_data.get('business_email', '')
        business_phone_number = user_data.get('business_phone_number', '')
        business_category_name = user_data.get('business_category_name', '')
        overall_category_name = user_data.get('overall_category_name', '')

        # Retornar os resultados
        return {
            "Full Name": full_name,
            "Facebook URL": facebook_url,
            "Is Private": is_private,
            "Is Verified": is_verified,
            "Business Address": business_address_json,
            "Business Contact Method": business_contact_method,
            "Business Email": business_email,
            "Business Phone Number": business_phone_number,
            "Business Category Name": business_category_name,
            "Overall Category Name": overall_category_name
        }
    else:
        # Retornar None se a resposta não for bem-sucedida
        return None

def display_profile_info(username, profile_picture_url, bio, num_posts, num_followers, num_following, external_url):
    print_colored(f"\nUsername: {username}", Fore.YELLOW)
    print_colored(f"Profile Picture URL: {profile_picture_url}", Fore.BLUE)
    print_colored(f"Number of Posts: {num_posts}", Fore.BLUE)
    print_colored(f"Number of Followers: {num_followers}", Fore.BLUE)
    print_colored(f"Number of Following: {num_following}", Fore.BLUE)
    if bio:
        print_colored(f"Bio: {bio}", Fore.BLUE)
    else:
        print_colored("Bio: N/A", Fore.BLUE)
    if external_url:
        print_colored(f"External URL: {external_url}", Fore.BLUE)
    else:
        print_colored("External URL: N/A", Fore.BLUE)

def check_for_changes_in_db(user_id, username, profile_picture_url, bio, num_posts, num_followers, num_following, external_url,
                            full_name, facebook_url, is_private, is_verified,
                            business_address, business_contact_method, business_email,
                            business_phone_number, business_category_name, overall_category_name):
    conn = sqlite3.connect('instagram_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM instagram_profiles WHERE user_id = ?
    ''', (user_id,))

    existing_data = cursor.fetchone()

    if existing_data:
        # Check for changes in each field
        changes_detected = False

        field_names = ['user_id', 'username', 'profile_picture_url', 'bio', 'num_posts', 'num_followers', 'num_following', 'external_url',
                       'full_name', 'facebook_url', 'is_private', 'is_verified',
                       'business_address', 'business_contact_method', 'business_email',
                       'business_phone_number', 'business_category_name', 'overall_category_name']

        for i, field_name in enumerate(field_names):
            if existing_data[i] != locals()[field_name]:
                changes_detected = True
                spinning_animation()
                print(f"\n{Fore.RED}{field_name} changed: {existing_data[i]} -> {locals()[field_name]}{Style.RESET_ALL}")

        if not changes_detected:
            print_colored(MSG_NO_CHANGES, Fore.GREEN)
        else:
            spinning_animation()
            print_colored(MSG_CHANGES_DETECTED, Fore.YELLOW)

            # Save the profile picture with good quality
            saved_image_path = save_profile_picture(profile_picture_url, username)

            if saved_image_path:
                print_colored(f"Profile picture saved at: {saved_image_path}", Fore.CYAN)

            # Update data in the database with new values and current timestamp
            profile_info = (user_id, username, profile_picture_url, bio, num_posts, num_followers, num_following, external_url,
                            full_name, facebook_url, is_private, is_verified,
                            business_address, business_contact_method, business_email,
                            business_phone_number, business_category_name, overall_category_name)
            update_data_in_db(*profile_info)
    else:
        print_colored(MSG_USER_NOT_FOUND, Fore.YELLOW)

    conn.close()

#####| Funções de Monitoramento e Logs - Monitoring Functions and Logs |#####

def monitor_profile(user_id, session_id, duration):
    start_time = time.time()
    end_time = start_time + duration

    while time.time() < end_time:
        animate_loading()
        profile_info = find_instagram_profile(user_id, session_id)

        if profile_info:
            display_profile_info(*profile_info)
            additional_data = extract_instagram_data(profile_info[0], session_id)

            if additional_data:
                for key, value in additional_data.items():
                    print_colored(f"{key}: {value}", Fore.BLUE)

                all_data = (*profile_info[:7], *additional_data.values())
                insert_data_to_db(user_id, *all_data)
                check_for_changes_in_db(user_id, *all_data)
                save_monitoring_log(user_id, *all_data)

                # Aguarde um intervalo antes de consultar novamente - Wait for a period of time before querying again #
                time.sleep(300)  # Intervalo de 300 segundos - 300 second interval #

            else:
                print_colored("Unable to retrieve additional Instagram data.", Fore.RED)
                break
        else:
            print_colored("Unable to retrieve profile.", Fore.RED)
            break

    print_colored(f"\nMonitoring completed. Duration: {duration} seconds", Fore.GREEN)


def save_monitoring_log(user_id, username, profile_picture_url, bio, num_posts, num_followers, num_following, external_url,
                        full_name, facebook_url, is_private, is_verified,
                        business_address, business_contact_method, business_email,
                        business_phone_number, business_category_name, overall_category_name):
    log_folder = "monitoring_logs"
    os.makedirs(log_folder, exist_ok=True)

    log_file_path = os.path.join(log_folder, f"{user_id}_monitoring_log.txt")

    with open(log_file_path, 'a') as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"\n\nTimestamp: {timestamp}\n")
        log_file.write(f"Username: {username}\n")
        log_file.write(f"Profile Picture URL: {profile_picture_url}\n")
        log_file.write(f"Bio: {bio}\n")
        log_file.write(f"Number of Posts: {num_posts}\n")
        log_file.write(f"Number of Followers: {num_followers}\n")
        log_file.write(f"Number of Following: {num_following}\n")
        log_file.write(f"External URL: {external_url}\n")
        log_file.write(f"Full Name: {full_name}\n")
        log_file.write(f"Facebook URL: {facebook_url}\n")
        log_file.write(f"Is Private: {is_private}\n")
        log_file.write(f"Is Verified: {is_verified}\n")
        log_file.write(f"Business Address: {business_address}\n")
        log_file.write(f"Business Contact Method: {business_contact_method}\n")
        log_file.write(f"Business Email: {business_email}\n")
        log_file.write(f"Business Phone Number: {business_phone_number}\n")
        log_file.write(f"Business Category Name: {business_category_name}\n")
        log_file.write(f"Overall Category Name: {overall_category_name}\n")

    print_colored(f"Monitoring log saved at: {log_file_path}", Fore.CYAN)


#####| A função principal que orquestra a execução do script - The main function that orchestrates script execution |#####

def main():
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'*' * 50}")
    print(f" Instagram Profile Viewer ")
    print(f" Script started at {current_time}")
    print(f"{'*' * 50}\n")

    session_id = load_session_id()

    if not session_id:
        session_id = input("Enter your Instagram session ID: ")
        save_session_id(session_id)

    print("\nSelect an option:")
    print("1. Search by user ID")
    print("2. Search by username")
    print("3. Display all data from the database")
    print("4. Monitor a profile for a specific duration")
    choice = input("Enter your choice: ")

    if choice == '1':
        user_id = input("Enter the user ID to search for: ")
        animate_loading()
        profile_info = find_instagram_profile(user_id, session_id)
        if profile_info:
            display_profile_info(*profile_info)

            # Call the new function to extract additional Instagram data
            additional_data = extract_instagram_data(profile_info[0], session_id)

            if additional_data:
                # Display the additional Instagram data
                for key, value in additional_data.items():
                    print_colored(f"{key}: {value}", Fore.BLUE)

                # Combine basic profile info and additional data for the function call
                all_data = (*profile_info[:7], *additional_data.values())

                # Insert data into the database
                insert_data_to_db(user_id, *all_data)

                # Check for changes in the database
                check_for_changes_in_db(user_id, *all_data)
            else:
                print_colored("Unable to retrieve additional Instagram data.", Fore.RED)
        else:
            print_colored("Unable to retrieve profile.", Fore.RED)
    elif choice == '2':
        username = input("Enter the username to search for: ")
        animate_loading()
        user_id = find_instagram_id_by_username(username)
        if user_id:
            print_colored(f"\nUser ID for {username}: {user_id}", Fore.YELLOW)

            # Display basic profile info first
            profile_info = find_instagram_profile(user_id, session_id)
            if profile_info:
                display_profile_info(*profile_info)

                # Extract and display additional Instagram data
                additional_data = extract_instagram_data(profile_info[0], session_id)

                if additional_data:
                    for key, value in additional_data.items():
                        print_colored(f"{key}: {value}", Fore.BLUE)

                    # Combine basic profile info and additional data for the function call
                    all_data = (*profile_info[:7], *additional_data.values())

                    # Insert data into the database
                    insert_data_to_db(user_id, *all_data)

                    # Check for changes in the database
                    check_for_changes_in_db(user_id, *all_data)
                else:
                    print_colored("Unable to retrieve additional Instagram data.", Fore.RED)
            else:
                print_colored("Unable to retrieve profile.", Fore.RED)
        else:
            print_colored("Unable to retrieve user ID.", Fore.RED)

    elif choice == '3':
        display_all_data_from_db()

    elif choice == '4':
        user_id = input("Enter the user ID to monitor: ")
        duration = int(input("Enter the duration to monitor (in seconds): "))
        monitor_profile(user_id, session_id, duration)
    else:
        print_colored("Invalid choice. Exiting.", Fore.RED)

    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    print(f"\n{'*' * 50}")
    print(f" Script completed in {elapsed_time} seconds")
    print(f"{'*' * 50}")

#####| Execução da Função Principal - Execution of the Main Function |#####
if __name__ == "__main__":
    main()

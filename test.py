
from scripts.load_from_ryans import load_from_ryans
from scripts.load_from_skyland import load_from_skyland
from scripts.load_from_startech import load_from_startech
from scripts.load_from_techland import load_from_techland


def print_menu():
    print("\nSmart Buy Scraper")
    print("----------------")
    print("1. Load from Techland")
    print("2. Load from Skyland") 
    print("3. Load from Startech")
    print("4. Load from Ryans")
    print("0. Exit")
    print("----------------")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice (0-3): ")

        if choice == "1":
            load_from_techland()
        elif choice == "2":
            load_from_skyland()
        elif choice == "3":
            load_from_startech()
        elif choice == "4":
            load_from_ryans()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
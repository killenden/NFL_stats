import sys
 
def main():
    if len(sys.argv) > 1:
        db_number = sys.argv[1]
        print(f"DB number received: {db_number}")
        # You can now use db_number in your script
    else:
        print("No DB number provided.")

if __name__ == "__main__":
    main()

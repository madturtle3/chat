import socklib

def main():
    client = socklib.Client()

    client.custom_parameters = {
        "username": input("USERNAME? ")
    }
    client.send("INITAL DATA SEND")

if __name__ == "__main__":
    main()

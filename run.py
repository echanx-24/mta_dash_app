from dashboard import create_dash

if __name__ == "__main__":
    app = create_dash()
    app.run(port="8080", debug=True)
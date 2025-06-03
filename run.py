from app import create_app  # Assuming you have a create_app function in your app/__init__.py file

# Initialize the Flask app
app = create_app()

if __name__ == '__main__':
    # Run the app in development mode
    app.run(debug=True)

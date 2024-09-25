from flask import Flask, render_template, request
import numpy as np
import pandas as pd

# Initialize the Flask app
app = Flask(__name__)

# Function to generate a random matrix as a Pandas DataFrame
def create_matrix(rows, cols, min_val, max_val):
    
    matrix = np.random.randint(min_val, max_val + 1, size=(rows, cols))
    return pd.DataFrame(matrix)

# Main page route to render the form in the index file
@app.route('/')
def index():
    
    return render_template('index.html')

# Route to handle form submission and display results
@app.route('/result', methods=['POST'])
def result():
    
    try:
        # Get inputs from the form for Matrix 1 and Matrix 2 dimensions and value ranges
        rows1 = int(request.form['rows1']) # rows1 is the value of the name attribute
        cols1 = int(request.form['cols1'])
        rows2 = int(request.form['rows2'])
        cols2 = int(request.form['cols2'])

        # Get min/max values for Matrix 1
        min_val1 = int(request.form['min_val1'])
        max_val1 = int(request.form['max_val1'])

        # Get min/max values for Matrix 2
        min_val2 = int(request.form['min_val2'])
        max_val2 = int(request.form['max_val2'])

        # Get the selected operation
        operation = request.form['operation']

        # Generate two random matrices by passing arguments based on user's inputs using Pandas library
        matrix1 = create_matrix(rows1, cols1, min_val1, max_val1)
        matrix2 = create_matrix(rows2, cols2, min_val2, max_val2)

        if operation == "add":
            # Check if both matrices have the same dimensions
            if matrix1.shape != matrix2.shape:
                raise ValueError("Error: Matrices must have the same dimensions for addition!")
            result_matrix = matrix1 + matrix2

        elif operation == "subtract":
            # Check if both matrices have the same dimensions
            if matrix1.shape != matrix2.shape:
                raise ValueError("Error: Matrices must have the same dimensions for subtraction!")
            result_matrix = matrix1 - matrix2

        elif operation == "multiply":
            # Check if number of columns in matrix 1 is equal to number of rows in matrix 2
            if cols1 != rows2:
                raise ValueError("Error: Matrix 1 columns must equal Matrix 2 rows for multiplication!")
            result_matrix = matrix1.dot(matrix2)

        elif operation == "divide":
            # Check if both matrices have the same dimensions
            if matrix1.shape != matrix2.shape:
                raise ValueError("Error: Matrices must have the same dimensions for division!")
            # Avoid division by zero
            result_matrix = matrix1 / matrix2.replace(0, np.nan)

        elif operation == "scalar_multiply":
            # Get the scalar value and the matrix choice
            scalar = float(request.form['scalar'])
            matrix_choice = request.form['matrix_choice']

            # Perform scalar multiplication based on the chosen matrix
            if matrix_choice == 'matrix1':
                result_matrix = matrix1 * scalar
            elif matrix_choice == 'matrix2':
                result_matrix = matrix2 * scalar
            else:
                raise ValueError("Error: Invalid matrix selection for scalar multiplication!")

        else:
            raise ValueError("Error: Invalid operation selected!")

        # In Flask, the render_template function is used to render the result file to the browser
        return render_template('result.html',
                               matrix1=matrix1.to_html(),# The to_html method is used to convert the matrix1 into an HTML format (a table) that can be displayed in the template directly
                               matrix2=matrix2.to_html(),
                               result_matrix=result_matrix.to_html(),
                               operation=operation)

    except Exception as e:
        # Handle any errors and display an error page
        return render_template('error.html', error=str(e))

# Chech if the script is being executed directly, run the app
if __name__ == '__main__':
    app.run(debug=True)

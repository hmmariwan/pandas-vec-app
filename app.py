from flask import Flask, render_template, request
import numpy as np
import pandas as pd

# Initialize the Flask app
app = Flask(__name__)

# Helper function to generate a random matrix as a Pandas DataFrame
def create_matrix(rows, cols, min_val, max_val):
    """
    Generates a random matrix as a Pandas DataFrame with the given number of rows and columns.
    The matrix is filled with random integers between min_val and max_val (inclusive).
    """
    matrix = np.random.randint(min_val, max_val + 1, size=(rows, cols))
    return pd.DataFrame(matrix)

# Main page route to render the form
@app.route('/')
def index():
    """
    Renders the index.html form to collect input from the user
    for the dimensions and values of the matrices.
    """
    return render_template('index.html')

# Route to handle form submission and display results
@app.route('/result', methods=['POST'])
def result():
    """
    Handles the POST request from the form, generates the matrices, 
    performs the selected operation, and displays the result. 
    If the operation is invalid, an error is shown.
    """
    try:
        # Get inputs from the form for Matrix 1 and Matrix 2 dimensions and value ranges
        rows1 = int(request.form['rows1'])
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

        # Generate two random matrices based on user inputs using Pandas
        matrix1 = create_matrix(rows1, cols1, min_val1, max_val1)
        matrix2 = create_matrix(rows2, cols2, min_val2, max_val2)

        if operation == "add":
            # Check if matrices are compatible for addition (same dimensions)
            if matrix1.shape != matrix2.shape:
                raise ValueError("Error: Matrices must have the same dimensions for addition!")
            result_matrix = matrix1 + matrix2

        elif operation == "subtract":
            # Check if matrices are compatible for subtraction (same dimensions)
            if matrix1.shape != matrix2.shape:
                raise ValueError("Error: Matrices must have the same dimensions for subtraction!")
            result_matrix = matrix1 - matrix2

        elif operation == "multiply":
            # Check if matrices are compatible for multiplication (Matrix 1 columns == Matrix 2 rows)
            if cols1 != rows2:
                raise ValueError("Error: Matrix 1 columns must equal Matrix 2 rows for multiplication!")
            result_matrix = matrix1.dot(matrix2)

        elif operation == "divide":
            # Check if matrices are compatible for division (same dimensions)
            if matrix1.shape != matrix2.shape:
                raise ValueError("Error: Matrices must have the same dimensions for division!")
            # Handle division carefully to avoid division by zero
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

        # Render the result page with the matrices and the result of the operation
        return render_template('result.html',
                               matrix1=matrix1.to_html(),
                               matrix2=matrix2.to_html(),
                               result_matrix=result_matrix.to_html(),
                               operation=operation)

    except Exception as e:
        # Handle any errors (such as invalid input) and display an error page
        return render_template('error.html', error=str(e))

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)

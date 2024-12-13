import lambda_function

interpreter, input_index, output_index = lambda_function.load_model()
result = lambda_function.predict('http://bit.ly/mlbookcamp-pants', interpreter, input_index, output_index)
print(result)

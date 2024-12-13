FROM public.ecr.aws/lambda/python:3.10

# Install system dependencies
RUN yum install -y mesa-libGL

# Install Python packages
RUN pip install --no-cache-dir keras-image-helper
RUN pip install --no-cache-dir "numpy<2"
RUN pip install --no-cache-dir https://github.com/alexeygrigorev/tflite-aws-lambda/raw/main/tflite/tflite_runtime-2.14.0-cp310-cp310-linux_x86_64.whl

# Copy your files
COPY clothing-model.tflite .
COPY lambda_function.py .

# Set permissions
RUN chmod 644 clothing-model.tflite

CMD [ "lambda_function.lambda_handler" ]
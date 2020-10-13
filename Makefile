build:
	zip -r lambda.zip * -x __pycache__ .git .gitignore
deploy:
	aws lambda update-function-code --function-name modeltexter --zip-file fileb://lambda.zip


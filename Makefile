test:
	echo "Running tests..."
	docker build -t test_ezmem . && docker run test_ezmem
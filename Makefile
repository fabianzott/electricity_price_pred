.DEFAULT_GOAL := default
.PHONY: set-credentials

#################### PACKAGE ACTIONS ###################
reinstall_package:
	@pip install -e .

# changes credentials path and environment name for users
set_credentials:
	@echo "Setting credentials and Python environment name. Choose user: fabian, nepomuk, oleksandr"; \
	read -p "Enter user name: " user_name; \
	if [ "$$user_name" = "fabian" ]; then \
		new_path="/home/fabian/code/fabianzott/gcp/electricity-price-prediction-5a0062f858b3.json"; \
		env_name="electricity_price_pred"; \
	elif [ "$$user_name" = "nepomuk" ]; then \
		new_path="/home/nepomuk/code/Nepomuk11/08-Project/electricity-price-prediction-f6c44aa442b0.json"; \
		env_name="elec_price_pred"; \
	elif [ "$$user_name" = "oleksandr" ]; then \
		new_path="/Users/sergeysechenov/code/electricity-price-prediction-ca60e85ef051.json"; \
		env_name="elec_price_pred"; \
	else \
		echo "Unknown user name. Enter custom credentials path."; \
		read -p "Enter custom credentials path: " new_path; \
		read -p "Enter custom Python environment name: " env_name; \
	fi; \
	sed -i 's|CREDENTIALS_PATH=.*|CREDENTIALS_PATH='"$$new_path"'|' .env; \
	echo $$env_name > .python-version

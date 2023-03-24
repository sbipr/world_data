import requests
import json
import worldometer
import psycopg2

print(worldometer.api.births_today())

# Set up connection to Amazon RDS instance
# Replace the values in the parentheses with your own database credentials
conn = psycopg2.connect(host='your-hostname',
                        user='your-username',
                        password='your-password',
                        database='your-database')

# Create separate tables for each API data in your Amazon RDS instance
# Replace the table names and column names as per your requirements
cur = conn.cursor()
cur.execute("CREATE TABLE population (country VARCHAR(255), population INT)")
cur.execute("CREATE TABLE deaths (country VARCHAR(255), deaths INT)")
cur.execute("CREATE TABLE births (country VARCHAR(255), births INT)")
cur.execute("CREATE TABLE government_economics (country VARCHAR(255), gdp FLOAT, inflation FLOAT)")
cur.execute("CREATE TABLE energy (country VARCHAR(255), oil_production FLOAT, oil_consumption FLOAT, coal_production FLOAT, coal_consumption FLOAT, natural_gas_production FLOAT, natural_gas_consumption FLOAT)")
cur.execute("CREATE TABLE health (country VARCHAR(255), life_expectancy FLOAT, fertility_rate FLOAT, infant_mortality_rate FLOAT)")
cur.execute("CREATE TABLE media (country VARCHAR(255), internet_users INT, mobile_subscribers INT)")
cur.execute("CREATE TABLE environment (country VARCHAR(255), co2_emissions FLOAT, forest_area FLOAT, annual_change_in_forest_area FLOAT)")
cur.execute("CREATE TABLE food (country VARCHAR(255), arable_land FLOAT, cereal_production INT, meat_production INT)")
cur.execute("CREATE TABLE water (country VARCHAR(255), total_renewable_water_resources FLOAT, freshwater_withdrawals FLOAT, total_desalinated_water_production FLOAT)")
cur.execute("CREATE TABLE education (country VARCHAR(255), literacy_rate FLOAT, school_life_expectancy INT, tertiary_education_enrollment FLOAT)")
cur.execute("CREATE TABLE transportation (country VARCHAR(255), roadways_length FLOAT, railways_length FLOAT, airports INT, merchant_marine_ships INT)")
conn.commit()

# Create a cursor object
cur = conn.cursor()

# Define API endpoints for each category
endpoints = {
    'population': 'https://api.worldometers.info/population',
    'deaths': 'https://api.worldometers.info/deaths',
    'births': 'https://api.worldometers.info/births',
    'government_economics': 'https://api.worldometers.info/government',
    'energy': 'https://api.worldometers.info/energy',
    'health': 'https://api.worldometers.info/health',
    'media': 'https://api.worldometers.info/media',
    'environment': 'https://api.worldometers.info/environment',
    'food': 'https://api.worldometers.info/food',
    'water': 'https://api.worldometers.info/water',
    'education': 'https://api.worldometers.info/education',
    'transportation': 'https://api.worldometers.info/transportation'
}

# Loop through endpoints and get data from APIs
for category, endpoint in endpoints.items():
    # Make request to API endpoint
    response = requests.get(endpoint)

    # Get JSON data from response
    data = response.json()

    # Extract data for each country and insert into PostgreSQL table
    for country_data in data:
        # Define INSERT statement for current category
        insert_statement = f"INSERT INTO {category} (country, value) VALUES (%s, %s)"

        # Extract country and value from current country's data
        country = country_data['country']
        value = country_data['value']

        # Execute INSERT statement with country and value
        cur.execute(insert_statement, (country, value))

        # Commit changes to database
        conn.commit()

# Close cursor and connection
cur.close()
conn.close()

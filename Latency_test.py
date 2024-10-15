import requests
import time
import csv
import matplotlib.pyplot as plt

# Function to perform latency testing
def run_performance_test(url, test_case, output_csv):
    times = []
    
    # Perform 100 API calls
    for i in range(100):
        start = time.time()  # Record start time
        response = requests.get(f'{url}?text={test_case}')
        end = time.time()  # Record end time
        
        # Record the time taken for the request
        latency = end - start
        times.append(latency)
        
        # Print and log each result for debugging
        print(f"API Call {i + 1}: {response.status_code} - Latency: {latency:.5f}s")
    
    # Save the results to a CSV file
    with open(output_csv, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Call Number', 'Time Taken (seconds)'])
        for i, t in enumerate(times):
            writer.writerow([i + 1, t])
    
    # Return the list of times for analysis
    return times

# Function to create boxplots for the results
def create_boxplot(csv_files, output_image):
    data = []
    
    # Read data from each CSV file
    for file in csv_files:
        times = []
        with open(file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                times.append(float(row[1]))
        data.append(times)
    
    # Generate the boxplot
    plt.boxplot(data)
    plt.xticks([1, 2, 3, 4], ['Test Case 1', 'Test Case 2', 'Test Case 3', 'Test Case 4'])
    plt.ylabel('Latency (seconds)')
    plt.title('API Latency Performance for Test Cases')
    
    # Save the boxplot as an image file
    plt.savefig(output_image)

# Main function to run the performance tests
if __name__ == '__main__':
    # Define the base URL for the API
    base_url = 'http://localhost:8080/predict'  # Change this to the AWS server URL if needed
    
    # Define the test cases (two fake news, two real news)
    test_cases = [
        ('This is real news', 'performance_data/real_news_1.csv'),
        ('Genuine report on environmental issues', 'performance_data/real_news_2.csv'),
        ('This is fake news', 'performance_data/fake_news_1.csv'),
        ('Totally fabricated story about celebrities', 'performance_data/fake_news_2.csv')
    ]
    
    csv_files = []
    
    # Run performance tests for each test case
    for test_case, csv_file in test_cases:
        print(f"Running performance test for: {test_case}")
        run_performance_test(base_url, test_case, csv_file)
        csv_files.append(csv_file)
    
    # Generate the boxplot for all test cases
    create_boxplot(csv_files, 'boxplots/api_latency_boxplot.png')

    # Print completion message
    print("Performance tests completed and boxplot generated.")

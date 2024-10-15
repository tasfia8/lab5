import requests
import time
import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Function to perform latency testing
def run_performance_test(url, test_case, output_csv):
    times = []
    
    # Open the CSV file and set up the writer
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        # Write the header with timestamps and latency
        writer.writerow(['Call Number', 'Timestamp', 'Time Taken (seconds)'])
        
        # Perform 100 API calls
        for i in range(100):
            start = time.time()  # Record start time in seconds
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # Record current timestamp
            response = requests.get(f'{url}?text={test_case}')
            end = time.time()  # Record end time
            
            # Record the time taken for the request (latency)
            latency = end - start
            times.append(latency)
            
            # Log the API call details
            print(f"API Call {i + 1}: {response.status_code} - Timestamp: {timestamp} - Latency: {latency:.5f}s")
            
            # Write the call number, timestamp, and latency to the CSV
            writer.writerow([i + 1, timestamp, latency])

    # Return the list of times (latency values) for further analysis
    return times

# Function to create boxplots and calculate the average performance, with annotations
def create_boxplot_and_calculate_average(csv_files, output_image):
    data = []
    averages = []
    
    # Read data from each CSV file
    for file in csv_files:
        times = []
        with open(file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                times.append(float(row[2]))  # Latency is in the 3rd column
        data.append(times)
        
        # Calculate and print the average latency for each test case
        average_latency = sum(times) / len(times)
        averages.append(average_latency)
        print(f"Average latency for {file}: {average_latency:.5f} seconds")
    
    # Generate the boxplot
    fig, ax = plt.subplots()
    ax.boxplot(data)
    ax.set_xticklabels(['Test Case 1', 'Test Case 2', 'Test Case 3', 'Test Case 4'])
    ax.set_ylabel('Latency (seconds)')
    ax.set_title('API Latency Performance for Test Cases')
    
    # Annotate the plot with the average latencies
    for i, avg in enumerate(averages, 1):
        ax.text(i, max(data[i-1]), f'Avg: {avg:.5f}s', horizontalalignment='center', fontsize=10, color='blue')
    
    # Save the boxplot as an image file
    plt.savefig(output_image)

    # Return the calculated averages for further use or display
    return averages

# Main function to run the performance tests
if __name__ == '__main__':
    # Define the base URL for the API (can be AWS Elastic Beanstalk URL or localhost)
    base_url = 'http://localhost:8080/predict'  # Use your Elastic Beanstalk URL if needed
    
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
    
    # Generate the boxplot and calculate average latency
    averages = create_boxplot_and_calculate_average(csv_files, 'boxplots/api_latency_boxplot.png')

    # Print the average latencies for all test cases
    for i, avg in enumerate(averages, 1):
        print(f"Test Case {i} Average Latency: {avg:.5f} seconds")

    # Print completion message
    print("Performance tests completed, averages calculated, and boxplot generated.")

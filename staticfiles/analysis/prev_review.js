document.addEventListener('DOMContentLoaded', () => {
    const dataPrev = prevRatings;
    const departments = Object.keys(dataPrev.departments); // Get the department names

    // Prepare the data for the chart
    const datasets = [];
    let labels = [];
    const totalDataPoints = 10;  // Always show 10 data points

    // Loop over departments to construct datasets
    departments.forEach(department => {
        const departmentData = dataPrev.departments[department];

        // Ensure the department has exactly 10 data points, filling with 0 for missing months
        let ratings = [];
        let departmentLabels = [];

        // Generate the labels for the last 10 months
        const now = new Date();
        for (let i = 0; i < totalDataPoints; i++) {
            const targetMonth = new Date(now);
            targetMonth.setMonth(now.getMonth() - (totalDataPoints - 1 - i));  // Go back (totalDataPoints-1-i) months

            const monthLabel = `${targetMonth.getFullYear()}-${(targetMonth.getMonth() + 1).toString().padStart(2, '0')}`;
            departmentLabels.push(monthLabel);  // Collect date labels

            // If there is data for the month, use it; otherwise, fill with 0
            const rating = departmentData[i] || 0;  // Directly use index from departmentData (0 is 10th month ago)
            ratings.push(rating);
        }

        // Set the labels from the first department (assumes all departments have the same dates)
        if (labels.length === 0) {
            labels = departmentLabels;  // Set labels only once
        }

        // Add the department's data to the dataset
        datasets.push({
            label: department, // Department name
            data: ratings, // Ratings data
            fill: false,
            borderColor: getRandomColor(), // Random color for each department
            tension: 0.1,
            color: 'whitesmoke',
        });
    });

    // Generate a random color for each department
    function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    // Create the chart
    const ctx = document.getElementById('line').getContext('2d');
    const ratingsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels, // Use the labels from the first department
            datasets: datasets,
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: 'whitesmoke', // Change the legend text color to whitesmoke
                    },
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return 'Avg Rating: ' + tooltipItem.raw.toFixed(2); // Display average rating
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Historical Departmental Reviews',
                    font: {
                        size: 18,
                        family: 'Arial',
                        weight: 'bold'
                    },
                    color: 'whitesmoke',  // Title text color
                    padding: {
                        top: 10,
                        bottom: 30
                    }
                },
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Month',
                        color: 'whitesmoke',
                    },
                    ticks: {
                        color: 'white',  // Change the x-axis tick color to white
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Average Rating',
                        color: 'whitesmoke',
                    }
                }
            }
        }
    });
});

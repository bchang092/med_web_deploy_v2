document.addEventListener('DOMContentLoaded', () => {
    // Importing data
    const dep_avgr_df = avg_dep_rating; // Contains avg_rating and department
    const department_sent = department_sentiments; // Sentiment data as a dictionary

    // Extract department names and average ratings
    const labels = dep_avgr_df.map(item => item.Department);  // Department names
    const avgData = dep_avgr_df.map(item => item.avg_rating); // Average ratings

    // Sentiment categories and their corresponding color mapping
    const sentimentCategories = ['Very Negative', 'Somewhat Negative', 'Neutral', 'Somewhat Positive', 'Very Positive'];
    const sentimentColors = [
        'rgba(255, 0, 0, 0.8)',       // Very Negative
        'rgb(255, 170, 0)',     // Somewhat Negative
        'rgb(0, 204, 255)',    // Neutral
        'rgba(208, 255, 0,1)',   // Somewhat Positive
        'rgb(0, 255, 0)'        // Very Positive
    ];

    // Initialize arrays for each sentiment
    const sentimentArrays = {
        "Very Negative": [],
        "Somewhat Negative": [],
        "Neutral": [],
        "Somewhat Positive": [],
        "Very Positive": []
    };
    
    dep_avgr_df.forEach(departmentObj => {
        const departmentName = departmentObj.Department; // Extract department name
        const sentiments = department_sent[departmentName]; // Get sentiment data for the department
    
        if (sentiments) {
            // Append sentiment values to the corresponding arrays
            Object.keys(sentimentArrays).forEach(category => {
                sentimentArrays[category].push(sentiments[category] || 0); // Add 0 if the sentiment value is missing
            });
        } else {
            console.warn(`No sentiment data found for department: ${departmentName}`);
            // Fill with 0s if department data is missing
            Object.keys(sentimentArrays).forEach(category => {
                sentimentArrays[category].push(0);
            });
        }
    });
    
    // Extra variables
    const text_color = 'whitesmoke';
    const cat_perc = 0.6;
    
    const data = {
        labels: labels,
        datasets: [
            { // Very Negative Sentiment
                label: 'Very Negative Sentiment',
                data: sentimentArrays['Very Negative'],
                backgroundColor: [sentimentColors[0]],
                categoryPercentage: cat_perc,
                xAxisID: 'x-axis-sentiment' // Use this axis for sentiment datasets
            },
            { // Somewhat Negative Sentiment
                label: 'Somewhat Negative Sentiment',
                data: sentimentArrays['Somewhat Negative'],
                backgroundColor: [sentimentColors[1]],
                categoryPercentage: cat_perc,
                xAxisID: 'x-axis-sentiment'
            },
            { // Neutral Sentiment
                label: 'Neutral Sentiment',
                data: sentimentArrays['Neutral'],
                backgroundColor: [sentimentColors[2]],
                categoryPercentage: cat_perc,
                xAxisID: 'x-axis-sentiment'
            },
            { // Somewhat Positive Sentiment
                label: 'Somewhat Positive Sentiment',
                data: sentimentArrays['Somewhat Positive'],
                backgroundColor: [sentimentColors[3]],
                categoryPercentage: cat_perc,
                xAxisID: 'x-axis-sentiment'
            },
            { // Very Positive Sentiment
                label: 'Very Positive Sentiment',
                data: sentimentArrays['Very Positive'],
                backgroundColor: [sentimentColors[4]],
                categoryPercentage: cat_perc,
                xAxisID: 'x-axis-sentiment'
            },
            { // Department Average Rating
                label: 'Department Average Rating',
                data: avgData,
                backgroundColor: ['rgba(112, 124, 130, 0.75)'],
                borderWidth: 1,
                grouped: false,
                order: 1,
                xAxisID: 'x-axis-average' // Use a different axis for average rating
            }
        ]
    };

    // Chart configuration
    const config = {
        type: 'bar',
        data,
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        font: { size: 14 },
                        color: text_color // White Smoke for legend labels
                    }
                },
                title: {
                    display: true,
                    text: 'Department Sentiments and Average Ratings',
                    color: text_color,
                    font: { size: 30 }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: text_color
                    }
                },
                'x-axis-sentiment': {
                    beginAtZero: true,
                    ticks: {
                        color: text_color
                    },
                    position: 'top', // Position the sentiment axis at the top
                    grid: {
                        drawOnChartArea: false // Hide grid lines for this axis
                    },
                    title: {
                        display: true,
                        text: 'Sentiment Counts',
                        color: 'whitesmoke',
                    }
                },
                'x-axis-average': {
                    beginAtZero: true,
                    ticks: {
                        color: text_color
                    },
                    position: 'bottom', // Position the average rating axis at the bottom
                    grid: {
                        drawOnChartArea: false // Hide grid lines for this axis
                    },
                    title: {
                        display: true,
                        text: 'Department Average Rating',
                        color: 'whitesmoke',
                    }
                },
              
            }
        }
    };

    // Render chart
    const myChart = new Chart(
        document.getElementById('horizChart'),
        config
    );

});

document.addEventListener('DOMContentLoaded', () => {
    // Use the global ratingDict variable from the HTML
    const rating_df = ratingDict;


    // Extract Rating labels and Occurrence counts
    const labels = rating_df.map(item => item.Rating);  // Rating labels
    const data = rating_df.map(item => item.Occurrences); // Occurrences for each rating


    // Define background colors for each rating section
    const backgroundColors = [
        'rgba(255, 0, 0)',            
        'rgba(255, 51, 51)',       
        'rgba(255, 102, 102)',      
        'rgba(255, 153, 153)',      
        'rgba(255, 204, 153)',      
        'rgba(255, 255, 102)',      
        'rgba(204, 255, 102)',      
        'rgba(153, 255, 102)',      
        'rgba(102, 255, 102)',      
        'rgba(0, 255, 0)'           
    ];


    const text_color = 'whitesmoke';


    // Calculate the maximum value of the data to set dynamic scaling for the y-axis
    const maxDataValue = Math.max(...data);
    const yAxisMax = maxDataValue;  // Add a 10% buffer to the max value for a little space


    // Create the chart
    const ctx = document.getElementById('bar');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColors,  // Use the predefined colors
                borderColor: '#ffffff',  // White border for the bars
                borderWidth: 2
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Overall Ratings Across All Departments',
                    font: {
                        size: 18,
                        family: 'Arial',
                        weight: 'bold'
                    },
                    color: text_color,  // Title text color
                    padding: {
                        top: 10,
                        bottom: 30
                    }
                },
                legend: {
                    display: false
                 },
                 tooltips: {
                    enabled: false
                 }
                
            },
            hover: {
                mode: 'nearest',  // Ensures that the nearest bar is targeted when hovered
                intersect: true    // Hover effect only activates when the cursor is over a bar
            },
            elements: {
                bar: {
                    hoverOffset: 10  // Increase the hover effect for the bar (how much the bar "pops" out)
                }
            },
            scales: {
                y: {
                    title: {
                        display: true,
                        text: 'Number of Reviews',
                        color: text_color,
                        font: {size: 14}
                    },
                    beginAtZero: true,
                    ticks: {color: text_color},
                },
                x: {
                    title: {
                        display: true,
                        text: 'Ratings',
                        color: text_color,
                        font: {
                            size: 14
                        }
                    },
                    beginAtZero: true,
                    ticks: {color: text_color},
                }
            }
        }
    });
});




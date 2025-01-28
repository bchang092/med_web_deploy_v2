document.addEventListener('DOMContentLoaded', () => {
    // Use the global ratingDict variable from the HTML
    const rev_df = depRevNum;
    console.log('depRevNum:', depRevNum);
  
    // Extract Rating labels and Occurrence counts
    const labels = rev_df.map(item => item.Department);  // Rating labels
    const data = rev_df.map(item => item.Occurrences);   // Occurrences for each rating
  
    // Function to generate a random color
    function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }
  
    // Generate a random color for each department
    const backgroundColors = labels.map(() => getRandomColor());
  
    const text_color = "whitesmoke";
    
    // Create the chart
    const ctx = document.getElementById('doughnut2');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColors,
                borderColor: '#ffffff',  // White border for the chart segments
                borderWidth: 2,
            }]
        },
        options: {
            layout: {
              padding: {
                top: 10,  // Adjust this value to control space from the top
                left: 20,  // Adjust this value to control space from the left
                right: 20, // Adjust this value to control space from the right
                bottom: 200,  // Adjust this value to control space from the bottom
              }
            },
            plugins: {
                title: {
                    display: false,
                },
                legend: {
                  display: true,
                  text: 'Ratings',
                  color: text_color,
                  font: {
                      size: 20
                  },
                  position: 'bottom',
                  labels: { // Add this section for label customization
                    color: text_color, // This controls the legend text color
                    font: {
                        size: 18
                    }
                  }
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
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
  // Use the global ratingDict variable from the HTML
  const sent_df = sentimentsDict;


  // Extract Rating labels and Occurrence counts
  const labels = sent_df.map(item => item.Sentiment);  // Rating labels
  const data = sent_df.map(item => item.Occurrences); // Occurrences for each rating

   // Define the correct order for sentiment labels
  const sentimentOrder = ['Very Negative', 'Somewhat Negative', 'Neutral', 'Somewhat Positive', 'Very Positive'];
  const sentimentColors = {
    'Very Negative': 'rgba(255, 0, 0, 0.8)', // Red
    'Somewhat Negative': 'rgba(255, 114, 0, 0.8)', // Orange
    'Neutral': 'rgba(190, 249, 255, 0.8)', // Light blue
    'Somewhat Positive': 'rgba(195, 255, 0, 0.8)', // Very light blue
    'Very Positive': 'rgba(0, 255, 47, 0.8)', // Light green
  };
  const backgroundColors = sent_df.map(item => sentimentColors[item.Sentiment]);

  const text_color ='rgba(199, 199, 234, 0.886)';
  
  // Calculate the maximum value of the data to set dynamic scaling for the y-axis

  // Create the chart
  const ctx = document.getElementById('doughnut');
  new Chart(ctx, {
      type: 'doughnut',
      data: {
          labels: labels,
          datasets: [{
              data: data,
              backgroundColor: backgroundColors,  // Use the predefined colors
              borderColor: '#ffffff',  // White border for the bars
              borderWidth: 2,
              circumference: 180,
              cutout:'70%',
              rotation: 270,
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
            },
              
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





const ctx = document.getElementById('myChart');

new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
      label: '# of Votes',
      data: [12, 19, 3, 5, 2, 3],
      backgroundColor: [
        'rgba(123,212,222, 0.5)',
        'red',
      ],
      borderWidth: 1
    }]
  },
  options: {
    title:{
        display: true,
        text: 'Expense per category2',
        
    },
  }
});

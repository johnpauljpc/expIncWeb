const renderChat =(data, labels) =>{

  const ctx = document.getElementById('myChart');

new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: labels,
    datasets: [{
      label: 'last 6 months expense',
      data: data,
      backgroundColor: [
        'rgba(123,212,222, 0.5)',
        'orange',
        'green',
        'blue',
        'pale',

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


}

const getChartData = ()=>{
  fetch('/expense-summary/')
  .then(res => res.json())
  .then(results=>{
    console.log('data', results)
    const category_data = results.expense_category_data
    const [labels, data] = [Object.keys(category_data),
    Object.values(category_data)]

    renderChat(data, labels)
    
  })
}


document.onload = getChartData()

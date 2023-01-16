mainTable = document.querySelector('.main-table')
tableOutput = document.querySelector('.table-output')
searchField = document.querySelector('#searchField')
pagination = document.querySelector("#pagination")
noResult = document.querySelector('.noResult')
results = document.querySelector('.t-body')


tableOutput.style.display = 'none'
mainTable.style.display = 'block'

searchField.addEventListener('keyup', (e) =>{
    searchVal = e.target.value
    tableOutput.style.display = 'none'
    noResult.style.display = 'none'
    results.innerHTML = ""
    mainTable.style.display = 'block'
    pagination.style.display = 'block'
    
    if(searchVal.trim().length > 0){
        mainTable.style.display = 'none'
        pagination.style.display = 'none'
        


        fetch('/income/search-income/', {
            method:"POST",
            body: JSON.stringify({searchText: searchVal}),
        }
        )
        .then((response) => response.json())
        .then((data) =>{
            
            if(data.length === 0){
                noResult.style.display =  'block'
                tableOutput.style.display = 'none'
            }
            else{
                noResult.style.display = "none"
                tableOutput.style.display = 'block'
                data.forEach((income) => {
                    results.innerHTML += `
                    <tr>
                    <td>${income.amount}</td>
                    <td>${income.source}</td>
                    <td>${income.description}</td>
                    <td>${income.date}</td>
                    <td><a href="{% url 'update-income' income.id%}" class="btn btn-sm btn-warning">Edit</a></td>
                </tr>
                    `
                   console.log(data) 
                });
            }
        })

    
    }


})
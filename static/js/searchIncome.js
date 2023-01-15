mainTable = document.querySelector('.main-table')
tableOutput = document.querySelector('.table-output')
searchField = document.querySelector('#searchField')


tableOutput.style.display = 'none'
mainTable.style.display = 'block'

searchField.addEventListener('keyup', (e) =>{
    searchVal = e.target.value
    console.log(searchVal)
})
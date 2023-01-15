const searchField = document.querySelector("#searchField");
const table_Output = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const tBody = document.querySelector(".t-body");
noReslt = document.querySelector('.noReslt')
table_Output.style.display = "none";

const pagination = document.querySelector(".pagination-container");

searchField.addEventListener("keyup", (e) => {
  const searchVal = e.target.value;
  if (searchVal.trim().length > 0) {
    pagination.style.display = "none";
    tBody.innerHTML = "";

    fetch("/search-expense/", {
      body: JSON.stringify({ searchText: searchVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data::>>", data);

        appTable.style.display = "none";
        table_Output.style.display = "block";

        if (data.length == 0) {
          table_Output.style.display = "none";
          noReslt.style.display = "block"
        } else {
            noReslt.style.display = 'none'
          data.forEach((item) => {
            tBody.innerHTML += `
            
                <tr>
                <td>${item.amount}</td>
                    <td>${item.category}</td>
                    <td>${item.description}</td>
                    <td>${item.date}</td>
                    <td> <a href="edit/${item.id}" class="btn btn-sm btn-warning">Edit</a></td>
                    <td> <a href="delete/${item.id}" class="btn btn-sm btn-danger">Delete</a></td>
                    </tr>
                    `;
          });
        }
      });
  } else {
    noReslt.style.display = 'none'
    table_Output.style.display = "none";
    pagination.style.display = "block";
    appTable.style.display = "block";
  }
});

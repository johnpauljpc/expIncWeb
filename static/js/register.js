const usernameField = document.querySelector("#usernameField")
const feedBackArea = document.querySelector(".feedback_invalid")
const emailField = document.querySelector("#emailField")
const password1Field = document.querySelector("#password1Field")
const password2Field = document.querySelector("#password2Field")
const feedback_Email_invalid = document.querySelector(".feedback_Email_invalid")
const feedback_valid = document.querySelector(".feedback_valid")
const checking = document.querySelector(".checking")
const showPass = document.querySelector(".showPass")
const submitButton = document.querySelector(".submitButton")

const pass1Val = password1Field.textContent
const pass2Val = password2Field.textContent 

const passwordToggleHandler = (e) =>{
    if (showPass.textContent === 'Show'){
        showPass.textContent = "Hide"
        password1Field.setAttribute('type', 'text')
        password2Field.setAttribute('type', 'text')
        //password2Field.setAttribute('type', 'text')

    }
    else{
        showPass.textContent = "Show"
        password1Field.setAttribute('type', 'password')
        password2Field.setAttribute('type', 'password')
    }
}

showPass.addEventListener('click', passwordToggleHandler )


usernameField.addEventListener("keyup", function(e){
    checking.style.display = "block"
    const usernameVal = e.target.value;
    
    
   
    checking.textContent = `checking  ${usernameVal}`
    
        
    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display = 'none';
    feedback_valid.style.display = "none"
    
    
    if(usernameVal.length > 0){
    fetch("/auth/validate-username/",{
    body: JSON.stringify({username:usernameVal}),
    method: "POST"
})
.then((res)=> res.json())
.then((data)=> {
    console.log("data", data)

    setTimeout(Timeout1, 1000)
    function Timeout1(){
    checking.style.display = "none"
    }
    
    if (data.username_error){
        // submitButton.disabled = true
        usernameField.classList.add("is-invalid");
        feedBackArea.style.display = 'block';
        feedBackArea.innerHTML = (`<p>${data.username_error}</p>`);

    }
    else{
        // submitButton.removeAttribute('disabled')
        feedback_valid.classList.add("is-valid")
        feedback_valid.style.display = "block"
        setTimeout(myTimeout1, 2000)
        
        
        function myTimeout1() {
            feedback_valid.innerHTML = `<b style=" color=black; "> correct</b>`
            feedback_valid.style.display = "none"
        }
    }
    
})
    }
})

emailField.addEventListener("keyup", (e)=>{
    emailVal = e.target.value
    console.log(emailVal)

    emailField.classList.remove("is-invalid")
    


    fetch('/auth/val-email/',{body:JSON.stringify({email:emailVal}),
    method: 'POST'
    }).then((res)=>res.json())

    .then((data)=>{
        console.log('data::>>', data)

        if(data.email_error){
            submitButton.disabled = true
            emailField.classList.add("is-invalid")
            
            feedback_Email_invalid.innerHTML=`${data.email_error}`

        }
        else{
            submitButton.removeAttribute('disabled')
        }
       
    })
})


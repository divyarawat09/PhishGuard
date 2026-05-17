function scrollToDetector(){
document.getElementById("detector").scrollIntoView({
behavior:"smooth"
});
}

async function analyzeURL(){

const url=document.getElementById("urlInput").value;

const resultCard=document.getElementById("resultCard");

const resultTitle=document.getElementById("resultTitle");

const resultText=document.getElementById("resultText");

const resultIcon=document.getElementById("resultIcon");

if(url===""){
alert("Please enter URL");
return;
}

try{

const response=await fetch("http://127.0.0.1:5000/predict",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
url:url
})

});

const data=await response.json();

resultCard.classList.remove("safe","warning","danger");

if(data.result==="Safe"){

resultCard.classList.add("safe");

resultIcon.innerHTML='<i class="fa-solid fa-shield-check"></i>';

resultTitle.innerText="Safe Website";

resultText.innerText="This website appears secure.";

}

else if(data.result==="Suspicious"){

resultCard.classList.add("warning");

resultIcon.innerHTML='<i class="fa-solid fa-triangle-exclamation"></i>';

resultTitle.innerText="Suspicious Website";

resultText.innerText="This URL looks suspicious.";

}

else{

resultCard.classList.add("danger");

resultIcon.innerHTML='<i class="fa-solid fa-skull-crossbones"></i>';

resultTitle.innerText="Dangerous Website";

resultText.innerText="High phishing risk detected.";

}

}

catch(error){

console.log(error);

alert("Backend connection failed");

}

}
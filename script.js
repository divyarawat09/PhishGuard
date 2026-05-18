function scrollToDetector(){
document.getElementById("detector").scrollIntoView({
behavior:"smooth"
});
}

async function analyzeURL(){

const url=document.getElementById("urlInput").value.trim();

const resultCard=document.getElementById("resultCard");

const resultTitle=document.getElementById("resultTitle");

const resultText=document.getElementById("resultText");

const resultIcon=document.getElementById("resultIcon");

if(url===""){
alert("Please enter URL");
return;
}

try{
resultCard.classList.remove("safe","warning","danger");
resultTitle.innerText="Analyzing...";
resultText.innerText="Please wait while we check this URL.";
resultIcon.innerHTML='<i class="fa-solid fa-spinner fa-spin"></i>';

const response=await fetch("http://127.0.0.1:5000/predict",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
url:url
})

});

if(!response.ok){
const errorData=await response.json().catch(()=>({error:"Unknown error"}));
throw new Error(errorData.error || "Request failed");
}

const data=await response.json();

resultCard.classList.remove("safe","warning","danger");

const confidenceText = data.confidence !== undefined
? ` (confidence: ${Math.round(data.confidence*100)}%)`
: "";

if(data.result==="Safe"){

resultCard.classList.add("safe");

resultIcon.innerHTML='<i class="fa-solid fa-shield-check"></i>';

resultTitle.innerText="Safe Website";

resultText.innerText=`This website appears secure${confidenceText}.`;

}

else if(data.result==="Suspicious"){

resultCard.classList.add("warning");

resultIcon.innerHTML='<i class="fa-solid fa-triangle-exclamation"></i>';

resultTitle.innerText="Suspicious Website";

resultText.innerText=`This URL looks suspicious${confidenceText}.`;

}

else{

resultCard.classList.add("danger");

resultIcon.innerHTML='<i class="fa-solid fa-skull-crossbones"></i>';

resultTitle.innerText="Dangerous Website";

resultText.innerText=`High phishing risk detected${confidenceText}.`;

}

}

catch(error){

console.log(error);
resultCard.classList.remove("safe","warning","danger");
resultCard.classList.add("warning");
resultIcon.innerHTML='<i class="fa-solid fa-triangle-exclamation"></i>';
resultTitle.innerText="Analysis Failed";
resultText.innerText=error.message || "Backend connection failed";

}

}
